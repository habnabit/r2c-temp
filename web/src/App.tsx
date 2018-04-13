import { Classes, Button } from '@blueprintjs/core';
import * as React from 'react';
import './App.css';
import 'normalize.css/normalize.css';
import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/icons/lib/css/blueprint-icons.css';

interface AppState {
  isAuthenticated: boolean;
  user?: string;
  docId?: string;
}

class App extends React.Component<{}, AppState> {
  constructor(props: {}) {
    super(props);

    this.state = {
      isAuthenticated: false,
    };
  }

  componentDidMount() {}

  submitNewName = (newName: string) => {};

  render() {
    return (
      <div className="App">
        {!this.state.isAuthenticated && (
          <HelloScreen submitNewName={this.submitNewName} />
        )}
      </div>
    );
  }
}

interface HelloProps {
  submitNewName: (newName: string) => void;
}

interface HelloState {
  name: string;
}

class HelloScreen extends React.Component<HelloProps, HelloState> {
  constructor(props: HelloProps) {
    super(props);
    this.state = {
      name: '',
    };
  }

  private onSubmitName() {
    this.props.submitNewName(this.state.name);
  }

  private onChangeName(e: React.FormEvent<HTMLInputElement>) {
    this.setState({ name: e.currentTarget.value });
  }

  public render() {
    return (
      <div className="screen hello-screen">
        <h1>Hi!</h1>
        <input
          className={Classes.INPUT}
          type="text"
          placeholder="Enter your name"
          dir="auto"
          value={this.state.name}
          onChange={this.onChangeName}
        />
        <Button onClick={this.onSubmitName}>Sign in</Button>
      </div>
    );
  }
}

export default App;
