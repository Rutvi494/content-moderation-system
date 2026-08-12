function ModerationResult({ result }) {
  if (!result) {
    return null;
  }

  return (
    <div className="result-card">
      <h2>Moderation Result</h2>

      <div
        className={`decision decision-${result.decision?.toLowerCase()}`}
      >
        {result.decision}
      </div>

      <div className="result-grid">
        <div>
          <span className="label">
            Risk Score
          </span>

          <span>
            {formatRiskScore(result.risk_score)}
          </span>
        </div>

        <div>
          <span className="label">
            User
          </span>

          <span>
            {result.user_id}
          </span>
        </div>

        <div>
          <span className="label">
            Moderation ID
          </span>

          <span className="small-text">
            {result.moderation_id}
          </span>
        </div>
      </div>

      <div className="reason">
        <strong>Reason:</strong>{" "}
        {result.reason}
      </div>

      <h3>Detected Moderation Labels</h3>

      {result.labels?.length > 0 ? (
        <div className="labels-container">
          {result.labels.map(
            (label, index) => (
              <div
                className="moderation-label"
                key={`${label.name}-${index}`}
              >
                <div>
                  <strong>
                    {label.name}
                  </strong>
                </div>

                {label.parent_name && (
                  <div>
                    Category:{" "}
                    {label.parent_name}
                  </div>
                )}

                <div>
                  Confidence:{" "}
                  {Number(
                    label.confidence
                  ).toFixed(2)}
                  %
                </div>
              </div>
            )
          )}
        </div>
      ) : (
        <p>
          No moderation labels were detected.
        </p>
      )}
    </div>
  );
}


function formatRiskScore(score) {
  if (score === undefined || score === null) {
    return "N/A";
  }

  return `${(Number(score) * 100).toFixed(0)}%`;
}


export default ModerationResult;