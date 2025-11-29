"""
Background worker for processing roast jobs asynchronously.
Uses threading with a simple queue system.
"""

import threading
import queue
import time
import uuid
from typing import Dict, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from app.services.model_client import get_model_client
from app.services.moderation import moderation
from app.utils.cache import cache
from app.config import settings


class JobStatus(str, Enum):
    """Job processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class RoastJob:
    """Roast job data."""
    job_id: str
    image_bytes: bytes
    status: JobStatus
    created_at: datetime
    result: Optional[Dict] = None
    error: Optional[str] = None


class RoastWorker:
    """Background worker for processing roast requests."""
    
    def __init__(self):
        self.job_queue = queue.Queue()
        self.jobs: Dict[str, RoastJob] = {}
        self.worker_thread: Optional[threading.Thread] = None
        self.running = False
        self._lock = threading.Lock()
        
        # Load prompts
        self.vision_prompt = self._load_prompt("vision_analyzer.txt")
        self.roast_prompt = self._load_prompt("roast_system.txt")
    
    def _load_prompt(self, filename: str) -> str:
        """Load prompt from file."""
        import os
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "..", "prompts", filename
        )
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback to simple prompts if files not found
            if "vision" in filename:
                return "Analyze this profile picture in detail. Describe what you see."
            else:
                return "Based on this profile picture, generate a witty, playful roast. Keep it funny but not mean."
    
    def start(self):
        """Start the worker thread."""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_jobs, daemon=True)
            self.worker_thread.start()
            print("🔥 Roast worker started")
    
    def stop(self):
        """Stop the worker thread."""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        print("🛑 Roast worker stopped")
    
    def submit_job(self, image_bytes: bytes) -> str:
        """
        Submit a new roast job.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Job ID for tracking
        """
        job_id = str(uuid.uuid4())
        
        job = RoastJob(
            job_id=job_id,
            image_bytes=image_bytes,
            status=JobStatus.PENDING,
            created_at=datetime.now()
        )
        
        with self._lock:
            self.jobs[job_id] = job
        
        # Add to queue
        self.job_queue.put(job_id)
        
        # Cache the pending status
        cache.set(f"job:{job_id}", {
            "status": JobStatus.PENDING,
            "created_at": job.created_at.isoformat()
        }, ttl=settings.CACHE_TTL)
        
        return job_id
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """
        Get the status of a job.
        
        Args:
            job_id: Job identifier
            
        Returns:
            Job status dictionary or None
        """
        # Try cache first
        cached = cache.get(f"job:{job_id}")
        if cached:
            return cached
        
        # Check in-memory jobs
        with self._lock:
            job = self.jobs.get(job_id)
        
        if not job:
            return None
        
        result = {
            "status": job.status,
            "created_at": job.created_at.isoformat()
        }
        
        if job.status == JobStatus.COMPLETED and job.result:
            result["result"] = job.result
        
        if job.status == JobStatus.FAILED and job.error:
            result["error"] = job.error
        
        # Cache the result
        cache.set(f"job:{job_id}", result, ttl=settings.CACHE_TTL)
        
        return result
    
    def _process_jobs(self):
        """Worker thread main loop."""
        while self.running:
            try:
                # Get job from queue with timeout
                job_id = self.job_queue.get(timeout=1)
                
                # Process the job
                self._process_single_job(job_id)
                
            except queue.Empty:
                # No jobs, continue loop
                continue
            except Exception as e:
                print(f"❌ Worker error: {e}")
    
    def _process_single_job(self, job_id: str):
        """
        Process a single roast job.
        
        Args:
            job_id: Job identifier
        """
        with self._lock:
            job = self.jobs.get(job_id)
        
        if not job:
            return
        
        try:
            # Update status to processing
            job.status = JobStatus.PROCESSING
            cache.set(f"job:{job_id}", {
                "status": JobStatus.PROCESSING,
                "created_at": job.created_at.isoformat()
            }, ttl=settings.CACHE_TTL)
            
            print(f"🔄 Processing job {job_id}")
            
            # Validate image
            if settings.ENABLE_MODERATION:
                validation = moderation.validate_image(job.image_bytes)
                if not validation["valid"]:
                    raise ValueError(f"Image validation failed: {validation['reason']}")
            
            # Generate roast using AI
            model_client = get_model_client()
            result = model_client.generate_roast(
                job.image_bytes,
                self.vision_prompt,
                self.roast_prompt
            )
            
            # Moderate the generated roast
            if settings.ENABLE_MODERATION:
                moderation_result = moderation.moderate_roast(result["roast"])
                if not moderation_result["approved"]:
                    raise ValueError(f"Roast moderation failed: {moderation_result['reason']}")
            
            # Job completed successfully
            job.status = JobStatus.COMPLETED
            job.result = {
                "roast": result["roast"],
                "analysis": result.get("analysis", "")
            }
            
            # Cache the result
            cache.set(f"job:{job_id}", {
                "status": JobStatus.COMPLETED,
                "created_at": job.created_at.isoformat(),
                "result": job.result
            }, ttl=settings.CACHE_TTL)
            
            print(f"✅ Job {job_id} completed")
            
        except Exception as e:
            # Job failed
            job.status = JobStatus.FAILED
            job.error = str(e)
            
            cache.set(f"job:{job_id}", {
                "status": JobStatus.FAILED,
                "created_at": job.created_at.isoformat(),
                "error": job.error
            }, ttl=settings.CACHE_TTL)
            
            print(f"❌ Job {job_id} failed: {e}")


# Global worker instance
worker = RoastWorker()
