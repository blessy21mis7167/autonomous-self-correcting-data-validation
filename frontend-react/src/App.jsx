import { useState, useEffect } from 'react';

const sampleInputs = [
  'Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad',
  'Name: JANE SMITH\nEmail: jane.smith@yahoo.com\nPhone: (555) 123-4567\nAge: 32\nBlood Group: O+\nDate: 15-March-2000',
  'Name:Bob Johnson|Email:bob@gmail|Phone:9876543210|Age:45|BG:B-|DOB:01/01/1979'
];

function App() {
  const [rawInput, setRawInput] = useState(sampleInputs[0]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [stats, setStats] = useState(null);
  const [escalations, setEscalations] = useState([]);
  const [activeTab, setActiveTab] = useState('validator');
  const [fileUploadResult, setFileUploadResult] = useState(null);
  const [fileLoading, setFileLoading] = useState(false);

  // Load stats on mount
  useEffect(() => {
    loadStats();
  }, []);

  async function loadStats() {
    try {
      const response = await fetch('http://localhost:8000/api/stats');
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  }

  async function loadEscalations() {
    try {
      const response = await fetch('http://localhost:8000/api/escalations');
      if (response.ok) {
        const data = await response.json();
        setEscalations(data.items || []);
      }
    } catch (err) {
      console.error('Failed to load escalations:', err);
    }
  }

  async function handleValidate() {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const response = await fetch('http://localhost:8000/api/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_input: rawInput }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Request failed: ${response.status}`);
      }
      const data = await response.json();
      setResult(data);
      loadStats();
    } catch (err) {
      setError(err.message || 'Validation failed');
    } finally {
      setLoading(false);
    }
  }

  async function handleResolveEscalation(escalationId, approved) {
    try {
      const response = await fetch(`http://localhost:8000/api/escalations/${escalationId}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ escalation_id: escalationId, approved }),
      });
      if (response.ok) {
        loadEscalations();
        alert(`Escalation ${approved ? 'approved' : 'rejected'} successfully!`);
      }
    } catch (err) {
      alert(`Failed to resolve escalation: ${err.message}`);
    }
  }

  async function handleFileUpload(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    // Check file type
    if (!file.name.endsWith('.csv') && !file.name.endsWith('.txt') && !file.name.endsWith('.tsv')) {
      setError('Only CSV, TXT, or TSV files are supported');
      return;
    }

    setFileLoading(true);
    setError('');
    setFileUploadResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/validate-file', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Upload failed: ${response.status}`);
      }

      const data = await response.json();
      setFileUploadResult(data);
      loadStats();
    } catch (err) {
      setError(err.message || 'File upload failed');
    } finally {
      setFileLoading(false);
      // Reset file input
      event.target.value = '';
    }
  }

  function getConfidenceColor(score) {
    if (score >= 0.8) return '#4caf50';
    if (score >= 0.6) return '#ff9800';
    return '#f44336';
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>🔍 Autonomous Data Validation System</h1>
          <p>Self-Correcting Validation with CrewAI Agents</p>
        </div>
      </header>

      <nav className="tabs">
        <button
          className={`tab ${activeTab === 'validator' ? 'active' : ''}`}
          onClick={() => setActiveTab('validator')}
        >
          📝 Validator
        </button>
        <button
          className={`tab ${activeTab === 'file-upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('file-upload')}
        >
          📤 Upload File
        </button>
        <button
          className={`tab ${activeTab === 'escalations' ? 'active' : ''}`}
          onClick={() => { setActiveTab('escalations'); loadEscalations(); }}
        >
          ⚠️ Escalations
        </button>
        <button
          className={`tab ${activeTab === 'stats' ? 'active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >
          📊 Statistics
        </button>
      </nav>

      <main className="app-main">
        {/* Validator Tab */}
        {activeTab === 'validator' && (
          <div className="validator-section">
            <div className="input-container">
              <h2>Enter Raw Data</h2>
              <div className="sample-buttons">
                {sampleInputs.map((sample, idx) => (
                  <button
                    key={idx}
                    className="sample-btn"
                    onClick={() => setRawInput(sample)}
                  >
                    Sample {idx + 1}
                  </button>
                ))}
              </div>
              <textarea
                value={rawInput}
                onChange={(e) => setRawInput(e.target.value)}
                placeholder="Paste messy data here..."
                rows={8}
              />
              <button
                className="validate-btn"
                onClick={handleValidate}
                disabled={loading || !rawInput.trim()}
              >
                {loading ? '⏳ Validating...' : '✅ Validate Data'}
              </button>
            </div>

            {error && <div className="error-box">{error}</div>}

            {result && (
              <div className="result-container">
                <div className="status-bar">
                  <div className={`status ${result.final_report.status}`}>
                    {result.final_report.status === 'completed' ? '✓ Completed' : '⚠️ Requires Review'}
                  </div>
                  <div className="confidence-badge">
                    Confidence: {(result.final_report.average_confidence * 100).toFixed(1)}%
                  </div>
                </div>

                <div className="results-grid">
                  <section className="result-section">
                    <h3>✅ Corrected Data</h3>
                    <div className="data-display">
                      {Object.entries(result.corrected_data).map(([key, value]) => (
                        <div key={key} className="data-row">
                          <span className="label">{key}:</span>
                          <span className="value">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  </section>

                  <section className="result-section">
                    <h3>🔧 Corrections Applied</h3>
                    {result.correction_log.length > 0 ? (
                      <ul className="log-list">
                        {result.correction_log.map((log, idx) => (
                          <li key={idx} className="log-item">
                            <strong>{log.field}:</strong> {log.original} → {log.corrected}
                            <br />
                            <small>{log.reason}</small>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="empty-message">No corrections needed</p>
                    )}
                  </section>

                  <section className="result-section">
                    <h3>⚡ Confidence Scores</h3>
                    <div className="confidence-bars">
                      {Object.entries(result.confidence_scores).map(([field, score]) => (
                        <div key={field} className="confidence-bar-wrapper">
                          <span className="field-name">{field}</span>
                          <div className="bar-container">
                            <div
                              className="bar-fill"
                              style={{
                                width: `${score * 100}%`,
                                backgroundColor: getConfidenceColor(score),
                              }}
                            />
                          </div>
                          <span className="score">{(score * 100).toFixed(0)}%</span>
                        </div>
                      ))}
                    </div>
                  </section>

                  {result.validation_errors && Object.keys(result.validation_errors).length > 0 && (
                    <section className="result-section error-section">
                      <h3>❌ Validation Errors</h3>
                      <ul className="error-list">
                        {Object.entries(result.validation_errors).map(([field, error]) => (
                          <li key={field}><strong>{field}:</strong> {error}</li>
                        ))}
                      </ul>
                    </section>
                  )}

                  {result.escalations.length > 0 && (
                    <section className="result-section escalation-section">
                      <h3>⚠️ Escalations ({result.escalations.length})</h3>
                      <ul className="escalation-list">
                        {result.escalations.map((esc, idx) => (
                          <li key={idx} className="escalation-item">
                            <strong>{esc.field}</strong>
                            <br />Original: {esc.original}
                            <br />Suggested: {esc.corrected}
                            <br />Confidence: {(esc.confidence * 100).toFixed(1)}%
                            <br /><em>{esc.reason}</em>
                          </li>
                        ))}
                      </ul>
                    </section>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* File Upload Tab */}
        {activeTab === 'file-upload' && (
          <div className="file-upload-section">
            <div className="file-input-container">
              <h2>📤 Upload & Batch Validate</h2>
              <p>Upload a CSV or TXT file to validate multiple records at once</p>
              
              <div className="file-upload-area">
                <label htmlFor="file-input" className="file-label">
                  <div className="file-icon">📁</div>
                  <div className="file-text">
                    <strong>Click to upload or drag and drop</strong>
                    <p>CSV, TXT, or TSV (Max 10MB)</p>
                  </div>
                  <input
                    id="file-input"
                    type="file"
                    accept=".csv,.txt,.tsv"
                    onChange={handleFileUpload}
                    disabled={fileLoading}
                    className="file-input"
                  />
                </label>
              </div>

              <div className="file-info">
                <h3>Supported Formats:</h3>
                <ul>
                  <li><strong>CSV</strong> - Comma, tab, or pipe-separated values with headers</li>
                  <li><strong>TXT</strong> - One record per line with key:value or field:value format</li>
                  <li><strong>TSV</strong> - Tab-separated values</li>
                </ul>
              </div>

              <div className="file-example">
                <h3>Example CSV Format:</h3>
                <pre>name,email,phone,age,blood_group
John Doe,john@gmail.com,9876543210,25,AB
Jane Smith,jane@yahoo.com,(555) 123-4567,32,O+</pre>
              </div>

              <div className="file-example">
                <h3>Example TXT Format:</h3>
                <pre>Name:John Doe Email:john@gmail.com Phone:9876543210 Age:25
Name:Jane Smith Email:jane@yahoo.com Phone:(555) 123-4567 Age:32</pre>
              </div>
            </div>

            {error && <div className="error-box">{error}</div>}

            {fileUploadResult && (
              <div className="file-results-container">
                <div className="file-summary">
                  <div className="summary-stat">
                    <div className="stat-value">{fileUploadResult.total_records}</div>
                    <div className="stat-label">Total Records</div>
                  </div>
                  <div className="summary-stat success">
                    <div className="stat-value">{fileUploadResult.processed_records}</div>
                    <div className="stat-label">Processed</div>
                  </div>
                  <div className={`summary-stat ${fileUploadResult.failed_records > 0 ? 'error' : ''}`}>
                    <div className="stat-value">{fileUploadResult.failed_records}</div>
                    <div className="stat-label">Failed</div>
                  </div>
                </div>

                {fileUploadResult.validations && fileUploadResult.validations.length > 0 && (
                  <section className="file-results-section">
                    <h3>✅ Validation Results ({fileUploadResult.validations.length})</h3>
                    <div className="validations-table">
                      <table>
                        <thead>
                          <tr>
                            <th>Row</th>
                            <th>Status</th>
                            <th>Confidence</th>
                            <th>Escalations</th>
                            <th>Corrected Data</th>
                          </tr>
                        </thead>
                        <tbody>
                          {fileUploadResult.validations.map((validation, idx) => (
                            <tr key={idx} className={validation.has_escalations ? 'has-escalations' : ''}>
                              <td>{validation.row}</td>
                              <td>
                                <span className="badge badge-success">✓</span>
                              </td>
                              <td>
                                <span className="confidence-badge">{(validation.confidence * 100).toFixed(1)}%</span>
                              </td>
                              <td>
                                {validation.has_escalations ? (
                                  <span className="badge badge-warning">⚠️ Review</span>
                                ) : (
                                  <span className="badge badge-info">✓ OK</span>
                                )}
                              </td>
                              <td>
                                <small>{JSON.stringify(validation.corrected_data).substring(0, 50)}...</small>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </section>
                )}

                {fileUploadResult.errors && fileUploadResult.errors.length > 0 && (
                  <section className="file-results-section error-section">
                    <h3>❌ Failed Rows ({fileUploadResult.errors.length})</h3>
                    <ul className="error-list">
                      {fileUploadResult.errors.map((error, idx) => (
                        <li key={idx}>
                          <strong>Row {error.row}:</strong> {error.error}
                        </li>
                      ))}
                    </ul>
                  </section>
                )}
              </div>
            )}
          </div>
        )}
        {activeTab === 'escalations' && (
          <div className="escalations-section">
            <h2>Pending Escalations</h2>
            {escalations.length === 0 ? (
              <div className="empty-state">
                <p>✓ No pending escalations</p>
              </div>
            ) : (
              <div className="escalations-list">
                {escalations.filter(e => e.status === 'pending').map((esc) => (
                  <div key={esc.id} className="escalation-card">
                    <div className="escalation-header">
                      <h3>{esc.field_name}</h3>
                      <span className="confidence-badge">
                        {(esc.confidence_score * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="escalation-content">
                      <p><strong>Original Value:</strong> {esc.original_value}</p>
                      <p><strong>Suggested Correction:</strong> {esc.corrected_value}</p>
                      <p><strong>Reason:</strong> {esc.reason}</p>
                    </div>
                    <div className="escalation-actions">
                      <button
                        className="btn-approve"
                        onClick={() => handleResolveEscalation(esc.id, true)}
                      >
                        ✓ Approve
                      </button>
                      <button
                        className="btn-reject"
                        onClick={() => handleResolveEscalation(esc.id, false)}
                      >
                        ✗ Reject
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Statistics Tab */}
        {activeTab === 'stats' && (
          <div className="stats-section">
            <h2>System Statistics</h2>
            {stats ? (
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{stats.total_validations}</div>
                  <div className="stat-label">Total Validations</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.total_fields_corrected}</div>
                  <div className="stat-label">Fields Corrected</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.total_escalations}</div>
                  <div className="stat-label">Total Escalations</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.pending_escalations}</div>
                  <div className="stat-label">Pending Review</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{(stats.average_confidence_score * 100).toFixed(1)}%</div>
                  <div className="stat-label">Avg Confidence</div>
                </div>
              </div>
            ) : (
              <p>Loading statistics...</p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
