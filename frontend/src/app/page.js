'use client'

import React, { useState, useEffect } from 'react';

import UserInfo from '../components/UserInfo';
import FileUpload from '../components/FileUpload';
import FileList from '../components/FileList';
import TaskList from '../components/TaskList';
import Billing from '../components/Billing';


const MainPage = () => {
    const [tokens, setTokens] = useState(0);

    return (
        <div>
            <h1>Основная страница</h1>
            
            <UserInfo tokens={tokens} setTokens={setTokens} />
            <br />
            <FileUpload />
            <br />
            <FileList tokens={tokens} setTokens={setTokens}/>
            <br />
            <TaskList />
            <br />
            <Billing />
        </div>
    );
};

export default MainPage;