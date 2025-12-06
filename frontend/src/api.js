/**
 * API client for communicating with the backend.
 */

const getApiUrl = () => {
  const url = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url;
  }
  // If no protocol is provided, assume valid production URL implies https
  return `https://${url}`;
};

const API_BASE_URL = getApiUrl();

/**
 * Upload an image to get roasted
 * @param {File} file - Image file to upload
 * @returns {Promise<{job_id: string, status_url: string}>}
 */
export async function uploadImage(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/roast`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to upload image');
  }

  return await response.json();
}

/**
 * Check the status of a roast job
 * @param {string} jobId - Job identifier
 * @returns {Promise<{status: string, result?: object, error?: string}>}
 */
export async function checkRoastStatus(jobId) {
  const response = await fetch(`${API_BASE_URL}/api/roast/${jobId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to check status');
  }

  return await response.json();
}

/**
 * Poll for roast completion
 * @param {string} jobId - Job identifier
 * @param {number} maxAttempts - Maximum polling attempts
 * @param {number} interval - Polling interval in ms
 * @returns {Promise<object>} - Final job result
 */
export async function pollRoastCompletion(
  jobId,
  maxAttempts = 60,
  interval = 2000
) {
  for (let i = 0; i < maxAttempts; i++) {
    const status = await checkRoastStatus(jobId);

    if (status.status === 'completed') {
      return status;
    }

    if (status.status === 'failed') {
      throw new Error(status.error || 'Roast generation failed');
    }

    // Wait before next poll
    await new Promise(resolve => setTimeout(resolve, interval));
  }

  throw new Error('Roast generation timed out');
}
