import React, { Component } from "react";
import "@fortawesome/fontawesome-free/js/fontawesome";
import "@fortawesome/fontawesome-free/css/fontawesome.css";
import "@fortawesome/fontawesome-free/js/solid";
import "@fortawesome/fontawesome-free/js/regular";
import "@fortawesome/fontawesome-free/js/brands";

import "../static/Sidebar.css";
export default class Sidebar extends Component {
  render() {
    return (
      <div className="left-nav">
        <div className="left-nav-item">
          <div onClick={() => this.props.switchPage("ApplicationPage")}>
            <i className="fas fa-columns left-nav-icon" />
          </div>
          <div onClick={() => this.props.switchPage("SearchPage")}>
            <i className="fas fa-search left-nav-icon" />
          </div>
          <div onClick={() => this.props.switchPage("ManageResumePage")}>
            <i className="fas fa-folder left-nav-icon"></i>
          </div>
          <div onClick={() => this.props.switchPage("JobRecommendPage")}>
            <i className="fas fa-crosshairs left-nav-icon"></i>
          </div>
        </div>
      </div>
    );
  }
}
