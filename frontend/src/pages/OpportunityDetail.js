import React from 'react';

function OpportunityDetail() {
  return (
    <div className="page-shell">
      <div className="surface-card p-8 md:p-10">
        <span className="section-kicker">Opportunity</span>
        <h1 className="section-title mt-3">Opportunity Details</h1>
        <p className="section-lead mt-3 max-w-2xl">
          Detailed opportunity content will render here once the backend supplies the selected posting.
        </p>
      </div>
    </div>
  );
}

export default OpportunityDetail;
