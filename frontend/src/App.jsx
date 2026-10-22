import { useState } from "react";
import CostEstimateTab from "./components/CostEstimateTab.jsx";
import ImmigrationTab from "./components/ImmigrationTab.jsx";
import Tabs from "./components/Tabs.jsx";

export default function App() {
  const [activeTab, setActiveTab] = useState("estimate");

  return (
    <div className="app">
      <header>
        <h1>Assignment cost estimate: Switzerland → UK</h1>
        <p>
          What it costs a Swiss employer to send one employee to its UK subsidiary
          for two years, and what the move involves.
        </p>
      </header>

      <Tabs active={activeTab} onChange={setActiveTab} />

      {/* Both panels stay mounted so the form keeps its values when the
          visitor switches tabs and comes back. */}
      <section
        id="panel-estimate"
        role="tabpanel"
        aria-labelledby="tab-estimate"
        hidden={activeTab !== "estimate"}
      >
        <CostEstimateTab />
      </section>
      <section
        id="panel-immigration"
        role="tabpanel"
        aria-labelledby="tab-immigration"
        hidden={activeTab !== "immigration"}
      >
        <ImmigrationTab />
      </section>
    </div>
  );
}
