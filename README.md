# roadmap

Allows you to create multiple roadmaps for your projects and displays them in a timeline

### Features:
- multiple roadmaps
- admin area for editing
- expandable cards
- milestones
- tasks
- subtasks
- descriptions for each task and subtask
- progress bar for upcoming, currently not finished, milestones
- separated api server and client (webserver) for rendering the roadmaps

### Installation

#### API Server
1. Set up a fresh PostgreSQL database.
2. Install the API server pipenv `pipenv install`
3. Adjust your settings in `settings.json`  
  -  `keyfile` and `certfile` in the section `server` must only be filled if `useSSL` is set to `true`.  
  - `secret` must be filled with a random string to ensure a secure login.

#### Client (Renders the roadmaps)
1. Install the Client pipenv `pipenv install`
3. Copy `settings-example.json` to `settings.json`
3. Adjust your settings in `settings.json`  
 - `keyfile` and `certfile` must only be filled if `useSSL` is set to `true`.  
 - `apiURL` needs to point ot the url where the API server is running (full url including the port).  
 - `secret` must be filled with a random string to ensure a secure login.

### Screenshots

![r1](https://cloud.githubusercontent.com/assets/16324894/19972309/e44dcede-a1e1-11e6-93f1-2f71f9df1b39.png)
![r2](https://cloud.githubusercontent.com/assets/16324894/19972312/e5574788-a1e1-11e6-991b-4165936dfd73.png)
![r3](https://cloud.githubusercontent.com/assets/16324894/19972313/e63d517e-a1e1-11e6-9470-5df08fadc09f.png)
