import { useState } from 'react';

const sampleInput = 'Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad';

function App() {
  const [rawInput, setRawInput] = useState(sampleInput);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleValidate() {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/api/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_input: rawInput }),
      });
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Validation failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <h1>Autonomous Self-Correcting Data Validation</h1>
      <p>Paste messy data and validate it through the backend API.</p>

      <textarea value={rawInput} onChange={(e) => setRawInput(e.target.value)} rows={10} />
      <button onClick={handleValidate} disabled={loading}>
        {loading ? 'Validating...' : 'Validate'}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result-grid">
          <section>
            <h2>Corrected Data</h2>
            <pre>{JSON.stringify(result.corrected_data, null, 2)}</pre>
          </section>
          <section>
            <h2>Validation Errors</h2>
            <pre>{JSON.stringify(result.validation_errors, null, 2)}</pre>
          </section>
          <section>
            <h2>Corrections</h2>
            <pre>{JSON.stringify(result.correction_log, null, 2)}</pre>
          </section>
          <section>
            <h2>Final Report</h2>
            <pre>{JSON.stringify(result.final_report, null, 2)}</pre>
          </section>
        </div>
      )}
    </div>
  );
}

export default App;
