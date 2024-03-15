'use client'
import React, { useState, useEffect } from 'react';
import { setCookie, getCookie, deleteCookie } from 'cookies-next';

const TaskList = () => {
    const [tasks, setTasks] = useState([]);

    
    const fetchTasks = async () => {
      let session = getCookie('session');
      fetch('/api/tasks/getall/' + session)
      .then(response => response.json())
      .then(response => setTasks(response.tasks));
    };
  
    useEffect(() => {
      fetchTasks();
      const intervalId = setInterval(fetchTasks, 1000); 
  
      return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <h3>Ваши задачи:</h3>
            <ul>
                {tasks.map((task) => (
                <li key={task.idx}>
                    <span>id: {task.idx} </span>
                    <span>{task.file} </span>
                    <span>{task.status} </span>
                    <span>{task.error && <p>{task.error}</p> } </span>
                </li>
                ))}
            </ul>
        </div>
    )
};

export default TaskList;