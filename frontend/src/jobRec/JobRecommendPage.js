import React, { useState, useEffect } from "react";
import $ from "jquery";
import "../static/resume.css";

function JobRecommendPage() {
  const [fileName, setFileName] = useState("");
  const [jobRecommendations, setJobRecommendations] = useState({});
  const [ setResumeDownloadContent] = useState("");

  useEffect(() => {
    // Fetch the data only after this component is mounted
    getFiles();
  }, []);

  const getFiles = () => {
    $.ajax({
      url: "http://localhost:5000/resume",
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Credentials": "true",
      },
      xhrFields: {
        responseType: "blob",
      },
      credentials: "include",
      success: (message, textStatus, response) => {
        setFileName(response.getResponseHeader("x-fileName"));
        setResumeDownloadContent(message);
      },
    });
  };

  const getRecommendation = () => {
    $.ajax({
      url: "http://localhost:5000/recommend",
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Credentials": "true",
      },
      contentType: "application/json",
      success: (response) => {
        let responseJson = JSON.parse(response);
        setJobRecommendations(responseJson);
      },
    });
  };

  useEffect(() => {
    console.log(jobRecommendations);
  }, [jobRecommendations]);

  return (
    <div style={{ marginTop: "10rem" }}>
      <h2>Uploaded Documents</h2>
      <table>
        <tbody>
          <tr>
            <th className="tablecol1">Documents</th>
            <th className="tablecol2">Actions</th>
          </tr>
          <tr>
            <td className="tablecol1">{fileName}</td>
            <td className="tablecol2">
              <button id="download" onClick={getRecommendation} type="button">
                Get Job Recommendations
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <h2 style={{ marginTop: "3rem", marginBottom: "2rem" }}>
        Job Recommendations
      </h2>
      <table>
        <tbody>
          <tr>
            <th className="tablecol2">Job Title</th>
            <th className="tablecol2">Name of the company</th>
            <th className="tablecol2">Career Page</th>
          </tr>
          {Object.keys(jobRecommendations).length > 0 &&
            jobRecommendations.jobs.map((job, index) => (
              <tr key={index}>
                <td className="tablecol2">{job.job_title}</td>
                <td className="tablecol2">{job.company_name}</td>
                <td className="tablecol2">
                  <a href={job.career_page}>{job.career_page}</a>
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

export default JobRecommendPage;
