// The two top-level tabs. Buttons with role="tab" and aria-selected keep this
// accessible without a tab library; the panels themselves live in App.jsx.

const TABS = [
  { id: "estimate", label: "Cost estimate" },
  { id: "immigration", label: "Immigration" },
];

export default function Tabs({ active, onChange }) {
  return (
    <div className="tabs" role="tablist">
      {TABS.map((tab) => (
        <button
          key={tab.id}
          type="button"
          role="tab"
          id={`tab-${tab.id}`}
          aria-selected={tab.id === active}
          aria-controls={`panel-${tab.id}`}
          className={tab.id === active ? "tab tab-active" : "tab"}
          onClick={() => onChange(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
