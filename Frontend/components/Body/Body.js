
import React, { useEffect, useState,useRef } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJs, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import axios from 'axios';
import './Body.css';

ChartJs.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export const Body = () => {
    const title = useRef("")
    const essay = useRef("")
    const [dataValue, setDataValue] = useState([])
    const [showBarChart, setShowBarChart] = useState(false)
    
    const [id,setId] = useState(0)
    const handleSubmit = async(e) => {
        e.preventDefault();
        const url = "http://127.0.0.1:5000/grade"
        const body = {title:title.current,essay:essay.current}
        try{
            const response = await axios.post(url, body,{
                headers:{ 'Content-Type':'application/json'}
            });
            const finalRes = response.data.essay_id;
            setId(finalRes);
        }
        catch(err){
            console.log(err);
        }
    }
    useEffect(() => {
        console.log(id);
        if(id!==0){
            fetchBarData();
            }
    }, [id]);
 
    console.log(title.current, essay.current)

    const options = {
        indexAxis: 'x',
        elements: {
            bar: {
                borderWidth: 2,
            }
        },
        responsive: true,
        plugins: {
            tooltip:{
                displayColor:false,
                backgroundColor:'#ffc107',
                borderColor: '#000',
                bodyColor: '#000',
                borderWidth: 1,
                titleColor:'#000',
                titleFont:'bold',
                titleFontSize: 30,
                yAlign:'bottom'

            },
            legend: {
                position: 'left',
            },
            title: {
                display: true,
                text: 'Bar chart..',
                titleFontSize:'30',
                titleFont:'bold',
                titleColor:'#000'
            }
        },
        scales: {
            x: {
                title: {
                    // font_size:"bold",
                    display: true,
                    text: 'Metrices'
                }
            }
    }
}

    const labels = ['Focus and Purpose', 'Content and Development', 'Organisation', 'Language use', 'Holistic Course']
    const data = {
        labels: labels,
        datasets: [{
            label: "result",
            data: dataValue,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)'
            ],
            borderWidth: 1
        }]
    }

    const fetchBarData = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/metrics/${id}`)
            const apiData = await response.data
            const resArr = []
            console.log(apiData);
            resArr.push(apiData.metrics.focus_and_development)
            resArr.push(apiData.metrics.content_development)
            resArr.push(apiData.metrics.organisation)
            resArr.push(apiData.metrics.language_use)
            resArr.push(apiData.metrics.Holistic_Score)
            setDataValue(resArr)
            setShowBarChart(true)

            // console.log(apiData)
            // console.log(dataValue)
        }
        catch (error) {
            console.error("error", error)
        }

    }

    return (
        <>
            <div className='container'>
                <form onSubmit={(e) => { handleSubmit(e) }} action='POST'>
                <div className="mb-3">
                        <label className="form-label">Title:</label>
                        <input
                         onChange={(e) => { title.current=e.target.value }}
                        //   value={title.current} 
                          className="form-control" id="title" name="title" />
                    </div>
                
                    <div className="mb-3">
                        <label className="form-label">Essay:</label>
                        <textarea onChange={(e) => { essay.current=e.target.value }} 
                        // value={essay.current} 
                        className="form-control" id="essay" name="essay" rows="5"></textarea>
                    </div>
                    <div className="d-grid gap-2">
                        <button 
                        // onClick={fetchBarData} 
                        className="btn btn-warning btn-lg" type="submit">Submit</button>
                    </div>

                </form>

                    {showBarChart ? <Bar data={data} options={options} /> : ""}
            </div>
        </>
    )
}

