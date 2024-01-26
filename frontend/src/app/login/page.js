    'use client'
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { setCookie, getCookie } from 'cookies-next';


const MainPage = () => {
    const router = useRouter();
    
    let session = getCookie('session');
    if(session){
        //session = JSON.parse()
        fetch('/api/sessions/verify?' + new URLSearchParams({"session_idx": session.session_idx}))
        .then((res) => res.json())
        .then((res) => {if(res.status == 'CORRECT_IDENTIFYER'){router.push('//');}})
    }

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail]       = useState('');

    const signup = async data => {
        try {
            console.log({name: username, password, email})
            let resp = await fetch('api/users', {
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
            console.log({name: username, password, email})
            let resp = await fetch('/api/sessions', {
                body: JSON.stringify({name: username, password, email}),
                method: "POST",
                headers: new Headers({"Content-Type": "application/json"})
            });
            if(resp.ok){
                let res = await resp.json();
                console.log(res);
                setCookie('session', res);
            }
            else{
                console.log(resp.status);
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
    </form>
    );
};

export default MainPage;