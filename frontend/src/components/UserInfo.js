'use client'
import React, { useState, useEffect } from 'react';
import { setCookie, getCookie, deleteCookie } from 'cookies-next';
import { useRouter } from 'next/navigation';

const UserInfo = ({tokens, setTokens}) => {
    const router = useRouter();

    const [userName, setUserName] = useState(null);

    React.useEffect(() => {
        const session = getCookie('session');

        if (!session) {
            router.push('/login');
        }

        const fetchUserId = async () => {
            try {
              const response = await fetch('/api/sessions/' + session);
              if(response.ok){
                const data = await response.json();
                const userId = data.user_idx;
                return userId;
              }
              else{
                router.push('/login');
              }
            } catch (err) {
                console.log(error);
            }
          };
      
          const fetchInfoById = async (userId) => {
            try {
              const response = await fetch(`/api/users/${userId}`);
              const data = await response.json();
              setUserName(data.name);
              setTokens(data.coins);
            } catch (err) {
              console.log(err)
              setError('Ошибка при получении имени пользователя: ' + err.message);
            }
          };
          
          const fetchUserInfo = async () => {
            fetchUserId().then((userId) => {
              if (userId) {
                fetchInfoById(userId);
              }
            });
          }

          fetchUserInfo();

          const intervalId = setInterval(fetchUserInfo, 1000);
  
          return () => clearInterval(intervalId);

    }, []);

    const handleLogout = () => {
      deleteCookie('session');
      router.push('/login');
  };

    return (
        <div>
            {userName ? `Привет, ${userName}!` : 'Загрузка...'}
            <br />
            {tokens != undefined ? `Токены: ${tokens}` : 'Загрузка...'}
            <br />
            <button onClick={handleLogout}>Выход</button>
        </div>
    )
};

export default UserInfo;