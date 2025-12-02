export default function Home() {
  return (
    <main style={{ padding: "2rem", fontFamily: "system-ui, sans-serif" }}>
      <h1>Geonosis</h1>
      <p>AI-powered software development orchestration</p>
      <div
        style={{
          marginTop: "1rem",
          padding: "0.5rem 1rem",
          backgroundColor: "#f0f0f0",
          borderRadius: "4px",
          display: "inline-block",
        }}
      >
        <span style={{ color: "#666" }}>Status:</span> Connecting to API...
      </div>
    </main>
  );
}
