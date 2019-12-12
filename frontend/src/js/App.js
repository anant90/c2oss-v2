import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, IndexRoute} from 'react-router';

import createBrowserHistory from 'history/lib/createBrowserHistory';

import Home from './components/Home';

import '!style!css!sass!../sass/main.sass';

class App extends React.Component{
	render(){
		return (
			<div className="main-container">
        <div className="body-container">
          {this.props.children}
        </div>
      </div>
		)
	}
};

ReactDOM.render((
	<Router history={createBrowserHistory()}>
		<Route path="/" component={App}>
			<IndexRoute component={Home} />
		</Route>
	</Router> 
), document.getElementById('app'));

export default App;