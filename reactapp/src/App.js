import logo from './logo.svg';
import './App.css';
import React from 'react'
import * as d3 from 'd3';
import BarChart from './BarChart';


function App() {
  return (
    <div>
      <Header />
      <Data />  
    </div>
  );
}


function Header() {
  return(
    <header>
      <h1 id='title'>Datatron Hex</h1>
    </header>
  )
}

function Data(){
  return(
    <div className='data-container'>
      <div>DATA</div>
      <div>DATA</div>
    </div>
  )
}


export default App;
