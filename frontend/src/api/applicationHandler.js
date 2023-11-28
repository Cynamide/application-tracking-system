import fetch from "./handler";

export const getApplications = () => {
  // console.log(params)
  return fetch({
    method: "GET",
    url: "/applications",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
  });
};

export const updateApplication = (appId, application) => {
  return fetch({
    method: "PUT",
    url: `/applications/${appId}`,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
    data: {
      application: application,
    },
  });
};

export const createApplication = (application) => {
  return fetch({
    method: "POST",
    url: "/applications",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
    body: {
      application: application,
    },
  });
};

export const deleteApplication = (appId, application) => {
  return fetch({
    method: "DELETE",
    url: "/applications",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    data: {
      application: application,
    },
  });
};
