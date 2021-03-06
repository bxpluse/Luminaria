import React, {useEffect, useState} from 'react';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import {BrowserRouter as Router, Link, Route, Switch} from 'react-router-dom';
import Select from 'react-select'
import Backup from './apps/backup/Backup';
import Graphy from './apps/graphy/Graphy';
import HealthCheck from './apps/health-check/HealthCheck';
import IPOStatus from './apps/ipos/IPOStatus';
import LogViewer from './apps/logviewer/LogViewer';
import News from './apps/news/News';
import Notes from './apps/notes/Notes';
import Pool from './apps/pool/Pool';
import RCStreamer from './apps/rc-streamer/RCStreamer';
import Signal from './apps/signal/Signal';
import TopTen from './apps/top-ten/TopTen';
import Updater from './apps/updater/Updater';
import Graph from './common/Graph';
import Socket from './components/Socket';
import Header from './pages/Header';
import Home from './pages/Home';
import Request from './Requests';
import AppUtil from './util/AppUtil'


function Navigation() {

    const [apps, setApps] = useState({});

    useEffect(() => {
        Request.POST_JSON('/get-all-apps', {}).then(data => {
            const applications = [];
            for (const [, app] of Object.entries(data)) {
                applications.push(app);
            }
            applications.sort(function(a, b){
                return a.order - b.order;
            });
            setApps(applications);
        });
    }, []);

    return (
        <React.Fragment>
            <Router>
                {
                    AppUtil.getCurrentApp() !== 'graph' ?
                        <>
                            <Header/>
                            <CustomNavBar apps={apps}/>
                        </>
                        : null
                }
                <Socket/>
                <div className="content py-5 bg-light">
                    <Switch>
                        <Route path="/graph">
                            <Graph />
                        </Route>
                        <Route path="/updater">
                            <Updater />
                        </Route>
                        <Route path="/logs">
                            <LogViewer apps={apps} />
                        </Route>
                        <Route path="/rc-streamer">
                            <RCStreamer />
                        </Route>
                        <Route path="/backup">
                            <Backup />
                        </Route>
                        <Route path="/ipos">
                            <IPOStatus />
                        </Route>
                        <Route path="/top-ten">
                            <TopTen />
                        </Route>
                        <Route path="/news">
                            <News />
                        </Route>
                        <Route path="/notes">
                            <Notes />
                        </Route>
                        <Route path="/pool">
                            <Pool />
                        </Route>
                        <Route path="/health-check">
                            <HealthCheck />
                        </Route>
                        <Route path="/signal">
                            <Signal />
                        </Route>
                        <Route path="/graphy">
                            <Graphy />
                        </Route>
                        <Route path="/">
                            <Home apps={apps} />
                        </Route>
                    </Switch>
                </div>
            </Router>
        </React.Fragment>
    );
}

function CustomNavBar(props) {

    const [fireworks, setFireworks] = useState({
        fire() {}
    });

    useEffect(() => {
        import('./components/Fireworks').then(Fireworks => {
            setFireworks(Fireworks);
        });
    }, []);

    const links = [];
    for(let i = 0; i < props.apps.length; i++){
        const app = props.apps[i];
        const is_link = app.url.includes('https');
        if(is_link){
            links.push(
                <NavDropdown.Item
                    key={'item_' + i}
                    href={app['url']}
                    target='_blank'
                    rel='noopener noreferrer'>
                    {app['name']}
                </NavDropdown.Item>,
                <NavDropdown.Divider key={'divider_' + i}/>
            )
        }
    }
    if(links.length > 0){
        links.pop();
    }

    return (
        <Navbar className={'custom-nav-bar navbar-expand-lg navbar-dark bg-dark'} bg="light" variant="light">

            <Link to="/">
                <Navbar.Brand>Home</Navbar.Brand>
            </Link>

            <Nav>
                <Nav.Link
                    onClick={() => {
                        for(let i = 0; i < 6; i++){
                            setTimeout(
                                () => fireworks.fire(),
                                Math.random() * 750
                            );
                        }}
                    }>Festival
                </Nav.Link>
            </Nav>

            <Nav>
                <NavDropdown id="nav-dropdown" title="External Links">
                    {links}
                </NavDropdown>
            </Nav>

            <Nav className="ml-auto">
                <Search apps={props.apps}/>
            </Nav>

        </Navbar>
    );
}


function Search(props) {

    const options = [];
    for(let i = 0; i < props.apps.length; i++){
        const app = props.apps[i];
        options.push(
            { value: app.name, label: app.name, url: app['link_to'] || app.url, is_link: app.url.includes('https')}
        )
    }

    const handleChange = (option) => {
        if(option.is_link) {
            window.open(option.url);
        } else {
            window.location.href = option.url;
        }
    };

    return (
        <div style={{width: "200px"}}>
            <Select options={options} onChange={handleChange} width='250px' />
        </div>
    );
}


export default Navigation;