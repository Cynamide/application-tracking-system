import React, { Component } from "react";
import { Modal } from "react-bootstrap";
import Button from "react-bootstrap/Button";
import { shareWithFriends } from "../api/share.js";

export default class ShareModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      applicationType: "Wishlist",
      emails: "",
      closeShareModal: props.closeShareModal,
      class: 1,
      submitDisabled: false,
    };
    this.selected = this.selected.bind(this);
    this.submit = this.submit.bind(this);
  }
  async submit() {
    const emailList = this.state.emails.split(",");
    const applicationClass = this.state.class;
    console.log(this.state.emails.split(","));
    console.log(this.state.class);
    this.setState({
      submitDisabled: true,
    });
    await shareWithFriends(emailList, applicationClass);
    this.setState({
      submitDisabled: false,
    });
    this.state.closeShareModal();
  }
  selected(event) {
    this.setState({ [event.target.id]: event.target.value }, () => {
      console.log(this.state);
    });
  }
  render() {
    return (
      <div>
        <Modal show={this.props.show} onHide={this.state.closeShareModal}>
          <Modal.Header closeButton>
            <Modal.Title>Share application status</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div>
              <div className="input-group mb-3">
                <div className="input-group-prepend">
                  <label className="input-group-text" htmlFor="class">
                    Application Type
                  </label>
                </div>
                <select
                  className="custom-select"
                  id="class"
                  value={this.state.class}
                  onChange={this.selected}
                >
                  <option>Choose...</option>
                  <option value="1">Wish list</option>
                  <option value="2">Waiting Referral</option>
                  <option value="3">Applied</option>
                  <option value="4">Rejected</option>
                </select>
              </div>
            </div>
            <div>
              <div>Enter emails in comma separated</div>
              <input
                type="text"
                className="form-control"
                id="emails"
                onChange={this.selected}
              />
            </div>
            <br />
            <Button
              variant="primary"
              onClick={this.submit}
              disabled={this.state.submitDisabled}
            >
              submit
            </Button>
          </Modal.Body>
        </Modal>
      </div>
    );
  }
}
