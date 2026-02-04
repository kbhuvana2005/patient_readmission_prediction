// predictionService.js

/**
 * Dummy prediction function
 * @param {Object} data - all medical fields
 * @returns {Promise<{ predicted: string, confidence: number }>}
 */
export function predictReadmission(data) {
  return new Promise((resolve) => {
    // Simulate API call delay
    setTimeout(() => {
      const predicted = Math.random() > 0.5 ? "Yes" : "No";
      const confidence = parseFloat((Math.random() * 0.3 + 0.7).toFixed(2)); // 0.7-1.0
      resolve({ predicted, confidence });
    }, 1000);
  });
}

// for api integration
/*
export async function predictReadmission(data) {
  const response = await fetch("http://your-api-endpoint", {
    method: "POST",
    body: JSON.stringify(data),
    headers: { "Content-Type": "application/json" }
  });
  return response.json();
}
*/