import React from 'react';
import {Link} from 'react-router';
import HeroUnit from './Dashboard/HeroUnit';
import IssuesUnit from './Dashboard/IssuesUnit';

class Dashboard extends React.Component{
	constructor(){
		super();
		this.state = {
			user: {},
			issues: {
				issues: [],
				last_synced: null
			},
			isSyncing: false,
			isFetchingIssues: false,
			filters: ["bugs", "enhancements", "unassigned"],
			activeFilters: ["unassigned"]
		};

		this.getUser = this.getUser.bind(this);
		this.getIssues = this.getIssues.bind(this);
		this.onSyncButtonClick = this.onSyncButtonClick.bind(this);
		this.onFilterClick = this.onFilterClick.bind(this);
	}

	componentDidMount(){
		this.getUser();
		this.getIssues(this.state.activeFilters);
	}

	getUser(){
		fetch('/api/user/', {credentials: 'same-origin'}).then(response => {
			return response.json();
		}).then(json => {
			this.setState({user: json});
		}).catch(ex => {
			console.log("Exception in getUser: ", ex);
		})
	}

	getIssues(activeFilters){
		this.setState({isFetchingIssues: true});

		let options = {filters: activeFilters};
		let params = Object.keys(options)
											.map((key) => encodeURIComponent(key) + "=" + encodeURIComponent(options[key]))
											.join("&")
											.replace(/%20/g, "+");
		let url = '/api/issues' + "?" + params;

		fetch(url, {credentials: 'same-origin'}).then(response => {
			return response.json();
		}).then(json => {
			this.setState({issues: json, isFetchingIssues: false});
			this.getUser();
		}).catch(ex => {
			console.log("Exception in getIssues: ", ex);
			this.setState({isFetchingIssues: false});
		})
	}

	onSyncButtonClick(){
    this.setState({isSyncing: true});
    fetch('/api/refresh/', {credentials: 'same-origin'}).then(response => {
		}).catch(ex => {
			console.log("Exception in getUser: ", ex);
      this.setState({isSyncing: false});
		});
		setTimeout(() => {
			this.setState({isSyncing: false});
			this.getIssues(this.state.activeFilters);
		}, 5*60*1000)
  }

	onFilterClick(filter){
		let activeFilters = this.state.activeFilters;
		let index = activeFilters.indexOf(filter);
		if(index>-1) {
			activeFilters.splice(index, 1);
		} else {
			activeFilters.push(filter);
		}
		this.setState({activeFilters: activeFilters});
		this.getIssues(this.state.activeFilters);
	}

	render(){
		return (
			<div className="dashboard-page">
				<HeroUnit {...this.state.user} />
				<IssuesUnit
					issues={this.state.issues}
					onSyncButtonClick={this.onSyncButtonClick}
					isSyncing={this.state.isSyncing}
					isFetchingIssues={this.state.isFetchingIssues}
					shouldShowSyncButton={new Date() - new Date(this.state.user.last_synced) > 3*60*60*1000}
					onFilterClick={this.onFilterClick}
					filters={this.state.filters}
					activeFilters={this.state.activeFilters}/>
			</div>
		)
	}
};

export default Dashboard;
