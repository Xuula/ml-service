    'use client'
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { setCookie, getCookie } from 'cookies-next';


const MainPage = () => {

    const router = useRouter();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail]       = useState('');
    const [message, setMessage]   = useState('')
    
    const checkSession = async () => {
        
        let session = getCookie('session');
        console.log('Current session: ' + session + ', checking...');
        if(session){
            let resp = await fetch('/api/sessions/' + session);
            if(resp.ok){
                router.push('//');
            }
        }    
    }

    useEffect(() => {
        checkSession();
    }, []);

    const signup = async data => {
        try {
            console.log({name: username, password, email})
            let resp = await fetch('/api/users', {
                body: JSON.stringify({name: username, password, email}),
                method: "POST",
                headers: new Headers({"Content-Type": "application/json"})
            });
            if(resp.ok){
                let res = await resp.json();
                console.log(res);
            }
            else{
                console.log(resp.status);
            }
        } catch (error) {
            console.error(error);
        }
      };

      const login = async data => {
        try {
            let resp = await fetch('/api/sessions', {
                body: JSON.stringify({name: username, password, email}),
                method: "POST",
                headers: new Headers({"Content-Type": "application/json"})
            });
            if(resp.ok){
                let res = await resp.json();
                res = res.session_idx;
                console.log('OK, session ID: ' + res)
                setCookie('session', res);
                await checkSession();
            }
            else{
                console.log(resp.status);
                let msg = await resp.text();
                setMessage(msg);
            }
        } catch (error) {
            console.error(error);
        }
      };

    return (
    <form>
        <label> Имя пользователя: </label>
        <input name="username" value={username} onChange={(e) => setUsername(e.target.value)}/><br />

        <label> Пароль:</label>
        <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)}/> <br />

        <label> Email:</label>
        <input type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} /> <br />

        <input type="button" value="Зарегистрироваться" onClick={signup} />
        <input type="button" value="Войти" onClick={login} />
        <span>{message && <p>{message}</p>}</span>
    </form>
    );
};

export default MainPage;