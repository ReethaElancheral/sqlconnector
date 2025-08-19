import { useState } from "react";
import QuoteCard from "./components/QuoteCard";
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  const [quote, setQuote] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchQuote = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/quote"); // real-time API via Flask
      const data = await res.json();
      setQuote(data.quote);
    } catch (err) {
      console.error(err);
      setQuote("Error fetching quote");
    }
    setLoading(false);
  };

  return (
    <div className="container py-5">
      <h1 className="text-center mb-4">Random Quote Generator</h1>
      <QuoteCard quote={quote} loading={loading} />
      <div className="text-center mt-3">
        <button className="btn btn-primary" onClick={fetchQuote}>
          Get Random Quote
        </button>
      </div>
    </div>
  );
}

export default App;
