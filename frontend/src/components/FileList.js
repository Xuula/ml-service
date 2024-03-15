'use client'
import React, { useState, useEffect } from 'react';
import { setCookie, getCookie, deleteCookie } from 'cookies-next';

const FileList = ({tokens, setTokens}) => {
    const [files, setFiles] = useState([]);

    
    const fetchFiles = async () => {
      let session = getCookie('session');
      fetch('/api/documents/getall/' + session)
      .then(response => response.json())
      .then(response => setFiles(response.files));
    };
  
    useEffect(() => {
      fetchFiles();
      const intervalId = setInterval(fetchFiles, 1000); // Обновление списка файлов каждые 5 секунд
  
      return () => clearInterval(intervalId);
    }, []);

    

    const handleDownload = idx => {
      let session = getCookie('session');
      window.open(`/api/documents/download/${idx}?session_idx=${session}`)
    }

    const handleProcess = async (idx, model) => {
      if(tokens < 150){
        alert('Обработка стоит 150 токенов; пожалуйста, пополните счёт.')
        return
      }
      let session = getCookie('session');
      await fetch(`/api/documents/process/${idx}?model=${model}&session_idx=${session}`,
                  {method: 'POST'});
    }

    return (
        <div>
            <h3>Ваши файлы:</h3>
            <ul>
                {files.map((file) => (
                <li key={file.idx}>
                    <span>{file.name} </span>
                    <span>id: {file.idx}  </span>
                    <span><a onClick={() => handleDownload(file.idx)} download>Скачать</a> </span> 
                    <span><a onClick={() => handleProcess(file.idx, 'SVC')} download>Обработать (SVC)</a> </span> 
                    <span><a onClick={() => handleProcess(file.idx, 'MNB')} download>Обработать (MNB)</a> </span> 
                </li>
                ))}
            </ul>
        </div>
    )
};

export default FileList;