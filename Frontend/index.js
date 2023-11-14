import React from 'react';
import ReactDOM from 'react-dom/client'
import { Header } from './components/Header/Header'
import { Body } from './components/Body/Body'

import 'bootstrap/dist/css/bootstrap.min.css'

const App = () => {
    return(
        <>
        <Header/>
        <Body/>
        </>
    )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />)