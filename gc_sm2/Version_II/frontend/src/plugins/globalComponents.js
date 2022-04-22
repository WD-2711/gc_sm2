import BaseNav from "../components/BaseNav";
import BaseInput from "../components/BaseInput";
import BaseButton from "../components/BaseButton";
import BaseCheckbox from "../components/BaseCheckbox";
import Card from "../components/Card";
import BaseHeader from "../components/BaseHeader";
import BaseDropdown from "../components/BaseDropdown";
import BaseTable from "../components/BaseTable";
import StatsCard from "../components/StatsCard";
import BaseAlert from "../components/BaseAlert";


const GlobalComponents = {
  install(app) {
    app.component("base-nav", BaseNav);
    app.component("base-button", BaseButton);
    app.component("base-checkbox", BaseCheckbox);
    app.component("base-input", BaseInput);
    app.component("card", Card);
    app.component("base-header", BaseHeader);
    app.component("base-dropdown", BaseDropdown);
    app.component("base-table", BaseTable);
    app.component("stats-card", StatsCard);
    app.component("base-alert", BaseAlert);
  },
};

export default GlobalComponents;
