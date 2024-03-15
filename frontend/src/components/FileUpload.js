'use client'
import React, { useState, useEffect } from 'react';
import { setCookie, getCookie, deleteCookie } from 'cookies-next';

const FileUpload = () => {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (!file) {
          return;
        }
    
        const formData = new FormData();
        formData.append('file', file);

        const session = getCookie('session');
    
        try {
          const response = await fetch('/api/documents/upload/' + session, {
            method: 'POST',
            body: formData,
          });
    
          if (!response.ok) {
            throw new Error('Ошибка загрузки файла');
          }
    
          const data = await response.json();
          console.log(data);
        } catch (error) {
          console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" onChange={handleFileChange} />
            <button type="submit">Отправить</button>
        </form>
    )
};

export default FileUpload;