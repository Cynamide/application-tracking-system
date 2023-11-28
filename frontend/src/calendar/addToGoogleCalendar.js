import React, { Component } from "react";

export class AddToCalendar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      company: props.company,
      date: props.date,
      ctz: props.ctz,
      jobTitle: props.jobTitle,
    };
  }
  componentDidMount() {
    console.log("Component did mount");
    console.log(this.state.date);
    console.log(this.state);
  }
  generateCalendarLink() {
    const baseUrl = "https://calendar.google.com/calendar/render";
    const url = new URL(baseUrl);
    if (!this.state.date) return "";
    var date = this.state.date.replaceAll("-", "");
    console.log(date);
    const startDate = `${date}T160000`;
    const endDate = `${date}T170000`;
    url.searchParams.set("action", "TEMPLATE");
    url.searchParams.set("text", `Deadline for company: ${this.state.company}`);
    url.searchParams.set(
      "details",
      `Deadline for the company: ${this.state.company}
       JobTitle --> ${this.state.jobTitle}`,
    );
    url.searchParams.set("dates", `${startDate}/${endDate}`);
    url.searchParams.set("ctz", `${this.state.ctz}`);
    return url.toString();
  }
  render() {
    return (
      <div className="addToCalendar">
        <a href={this.generateCalendarLink()} target="_blank" rel="noreferrer">
          Add to google calendar
        </a>
      </div>
    );
  }
}
