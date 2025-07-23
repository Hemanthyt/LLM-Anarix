import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [resultText, setResultText] = useState("");
  const [chartUrl, setChartUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const delayPara = (index, nextWord) => {
    setTimeout(() => {
      setResultText((prev) => prev + nextWord);
    }, 75 * index);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResultText("");
    setChartUrl("");

    try {
      const queryRes = await axios.post("http://127.0.0.1:8000/ask-gemini/", {
        prompt,
      });

      const rawResponse = queryRes.data.response;
      const bodyStr = rawResponse.body; // This is a JSON string
      console.log("Response from server:", bodyStr);
      const data = JSON.parse(bodyStr); // Convert string to JSON
      console.log("Parsed data:", data);

      if (data.type === "chart") {
        setChartUrl(`data:image/png;base64,${data.image}`);
      } else if (data.type === "text") {
        const cleanContent = data.message.replace(/^"|"$/g, ""); // Remove outer quotes if any
        const words = cleanContent.split(" ");
        words.forEach((word, idx) => {
          delayPara(idx, word + " ");
        });
      }
    } catch (err) {
      console.error("Error:", err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-3xl w-full">
        <h1 className="text-3xl font-bold mb-6 text-center text-indigo-600">
          AI SQL Assistant
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
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
        {chartUrl && (
          <div className="mt-6">
            {chartUrl && (
              <img
                src={chartUrl}
                alt="Generated Chart"
                className="rounded-lg shadow-md"
              />
            )}
          </div>
        )}

        {resultText && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2 text-gray-700">
              Query Result:
            </h2>{" "}
            <div className="mt-4 p-4 bg-gray-100 rounded-md text-lg font-medium min-h-[3rem] whitespace-pre-wrap">
              {resultText}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
