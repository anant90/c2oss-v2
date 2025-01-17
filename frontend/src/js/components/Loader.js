import React from 'react';

export default class Loader extends React.Component{
	render() {
		return (
			<div className="loader">
				<svg className="circular" viewBox="25 25 50 50">
					<circle className="path" cx="50" cy="50" r="20" fill="none" strokeWidth="3" stroke={this.props.color ? this.props.color: "#4A90E2"}/>
				</svg>
			</div>
		)
	}
}
