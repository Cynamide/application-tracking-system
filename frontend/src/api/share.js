import fetch from "./handler";
export const shareWithFriends = (emailList, applicationClass) => {
  return fetch({
    method: "POST",
    url: "/share",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
    body: {
      email: emailList,
      type: applicationClass,
    },
  });
};
