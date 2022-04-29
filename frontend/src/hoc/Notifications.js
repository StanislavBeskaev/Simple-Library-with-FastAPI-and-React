import React from "react";
import NotificationList from "../components/notifications/NotificationList"

const withNotifications = Component => props => {
  return (
      <React.Fragment>
        <NotificationList />
        <Component {...props} />
      </React.Fragment>
  )
}

export default withNotifications