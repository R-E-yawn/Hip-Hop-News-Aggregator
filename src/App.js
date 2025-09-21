import logo from './logo.svg';
import './App.css';
import Feed from './components/Feed.jsx';
import Header from './components/Header.jsx';
import React, {useState, useEffect} from 'react';
import Markdown from 'markdown-to-jsx'
import { Routes, Route } from 'react-router-dom';
import Article from './components/Article.jsx';
import LoadPage from './components/LoadPage.jsx';
import Home from './components/Home.jsx';
import { Navigate } from 'react-router-dom';



export default function App() {   
  return (     
    <>       
      <Routes>         
        <Route path="/" element={<Home/>}/>  
        
        <Route path="/article/:mdFile" element={<Article/>}/>        
      </Routes>     
    </>        
  ); 
}


