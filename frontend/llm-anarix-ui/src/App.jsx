import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const queryRes = await axios.post("http://127.0.0.1:8000/ask-gemini/", {
        prompt,
      });

      const message = queryRes.data.response.message;
      setResult(message);
    } catch (error) {
      console.error(error);
      setResult("Error occurred. Check backend.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-3xl w-full">
        <h1 className="text-3xl font-bold mb-6 text-center text-indigo-600">
          AI SQL Assistant
        </h1>

        <form onSubmit={handleQuerySubmit} className="space-y-4">
          <textarea
            rows="3"
            placeholder="Ask something like: Total revenue for each product"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400"
            required
          />

          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 transition"
          >
            Generate & Run
          </button>
        </form>

        {loading && (
          <p className="text-center mt-4 text-gray-500">Loading...</p>
        )}

        {result && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2 text-gray-700">
              Query Result:
            </h2>
            <div className="bg-gray-200 p-3 rounded text-xl text-gray-800 text-center">
              {result}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
