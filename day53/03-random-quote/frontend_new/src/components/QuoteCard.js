function QuoteCard({ quote, loading }) {
  return (
    <div className="card mx-auto" style={{ maxWidth: "600px" }}>
      <div className="card-body">
        {loading ? (
          <div className="spinner-border text-primary" role="status"></div>
        ) : (
          <p className="card-text">{quote || "Click the button to get a quote"}</p>
        )}
      </div>
    </div>
  );
}

export default QuoteCard;
