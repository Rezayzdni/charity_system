import React from 'react'
import 'bootstrap/dist/css/bootstrap.css'
import './App.css'
import Authentication from './Pages/authentication'
import Tasks from './Pages/Tasks'
import BenefactorProfile from './Pages/BenefactorProfile'
import CharityProfile from './Pages/charityProfile'

import { Route, Redirect } from 'react-router-dom'

const ProtectedRoute = ({ component: Component, allow, ...rest }) => (
  <Route
    {...rest}
    render={(props) =>
      allow ? (
        <Component {...props} />
      ) : (
        <Redirect to="/tasks" />
      )
    }
  />
)


export default class App extends React.Component {
  render() {
    const isBenefactor = localStorage.getItem('is_benefactor') === 'true'
    const isCharity = localStorage.getItem('is_charity') === 'true'

    return (
      <div>
        <Route exact path="/" component={Authentication} />
        <Route path="/tasks" component={Tasks} />

        <ProtectedRoute
          exact
          path="/benefactor"
          component={BenefactorProfile}
          allow={isBenefactor}
        />

        <ProtectedRoute
          exact
          path="/charity"
          component={CharityProfile}
          allow={isCharity}
        />
      </div>
    )
  }
}
