import React, { Component } from "react";
import $ from "jquery";
import { getResumes, uploadResume } from "../api/getFiles.js";
import "../static/resume.css";

export default class ManageResumePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      fileName: "",
      fileuploadname: "",
    };

    console.log("***");
    console.log(localStorage.getItem("token"));
    this.getFiles.bind(this);
  }

  async getFiles() {
    const res = await getResumes();
    console.log(res);
    console.log("response headers", res.headers);
    this.setState({ fileName: "ResumeFile" });
    this.setState({ resumeDownloadContent: res });
  }
  handleChange(event) {
    var name = event.target.files[0].name;
    console.log(`Selected file - ${event.target.files[0].name}`);
    this.setState({ fileuploadname: name });
  }

  async uploadResume() {
    this.setState({ fileName: this.state.fileuploadname });
    console.log(this.value);
    const fileInput = document.getElementById("file").files[0];
    //console.log(fileInput);

    let formData = new FormData();
    formData.append("file", fileInput);
    //console.log(formData);

    const some = await uploadResume(formData);
    console(some, "after upload");
  }

  async downloadResume() {
    $.ajax({
      url: "http://localhost:3000/resume",
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Credentials": "true",
      },
      xhrFields: {
        responseType: "blob",
      },
      success: (message, textStatus, response) => {
        console.log(message);
        console.log(textStatus);
        console.log(response);

        var a = document.createElement("a");
        var url = window.URL.createObjectURL(message);
        a.href = url;
        a.download = "resume.pdf";
        document.body.append(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      },
    });
  }

  componentDidMount() {
    // fetch the data only after this component is mounted
    this.getFiles();
  }

  render() {
    return (
      <form
        class="pagelayout"
        id="upload-file"
        method="post"
        encType="multipart/form-data"
      >
        <input
          id="file"
          name="file"
          type="file"
          onChange={this.handleChange.bind(this)}
        ></input>
        <button
          id="upload-file-btn"
          onClick={this.uploadResume.bind(this)}
          type="button"
        >
          Upload
        </button>

        <div style={{ margin: 2 + "em" }}></div>
        <div>
          <h2>Uploaded Documents</h2>
          <table>
            <tr>
              <th class="tablecol1">Documents</th>
              <th class="tablecol2">Actions</th>
            </tr>
            <tr>
              <td class="tablecol1">{this.state.fileName}</td>
              <td class="tablecol2">
                <button
                  id="download"
                  onClick={this.downloadResume.bind(this)}
                  type="button"
                >
                  Download
                </button>
              </td>
            </tr>
          </table>
        </div>
      </form>
    );
  }
}
