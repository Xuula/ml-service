'use client'
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { setCookie, getCookie } from 'cookies-next';


const MainPage = () => {
    const router = useRouter();

    React.useEffect(() => {
        const sessionId = getCookie('sessionId');

        if (!sessionId) {
            router.push('/login');
        }
    }, []);

    return (
        <div>
            <h1>Основная страница</h1>
            {/* Остальной контент страницы */}
        </div>
    );
};

export default MainPage;