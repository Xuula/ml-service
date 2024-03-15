'use client'
import React, { useState, useEffect } from 'react';
import { setCookie, getCookie, deleteCookie } from 'cookies-next';

const Billing = () => {
    const [tokensToPut, setTokensToPut] = useState(0);

    const handlePutTokens = async () => {
        let session = getCookie('session');
        await fetch(`/api/users/coins/${session}?coins_num=${tokensToPut}`,
        {method: 'PUT'});
        setTokensToPut(0);
    }

    return (
        <div>
            <h3>Биллинг:</h3>
            <span>Количество токенов: </span>
            <input name="tokens" value={tokensToPut} onChange={(e) => setTokensToPut(e.target.value)}/><br />
            <input type="button" value="Положить на счёт" onClick={handlePutTokens} />
        </div>
    )
};

export default Billing