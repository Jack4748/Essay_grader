
import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJs, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import axios from 'axios';
import './Body.css';

ChartJs.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export const Body = () => {
    const [title, setTitle] = useState("")
    const [essay, setEssay] = useState("")

    const handleSubmit = (e) => {
        e.preventDefault();
        const url = "http://127.0.0.1:5000/add-data"
        axios.post(url, { title: title, essay:essay })
            .then(res => { console.log(res) })
            .catch(err => { console.log(err) })

    }
    
    const [dataValue, setDataValue] = useState([])
    const [showBarChart, setShowBarChart] = useState(false)
    console.log(title, essay)

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
    }

    const labels = ['Focus and Purpose', 'Content and Development', 'Organisation', 'Language use', 'Holistic Course']
    const data = {
        labels: labels,
        datasets: [{
            label: "Dataset",
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
            // const response = await fetch("http://127.0.0.1:5000/send-data")
            // const apiData = await response.json();
            // setDataValue(apiData)

            const response = await axios.get("https://jsonplaceholder.typicode.com/users")
            const apiData = await response.data
            setDataValue(apiData.map((ele)=> ele.id))
            setShowBarChart(true)

            console.log(apiData)
            console.log(dataValue)
        }
        catch (error) {
            console.error("error", error)
        }

    }

    // useEffect(()=>{fetchBarData()},[])

    return (
        <>
            <div className='container'>
                <form onSubmit={(e) => { handleSubmit(e) }} action='POST'>
                <div className="mb-3">
                        <label className="form-label">Title:</label>
                        <input onChange={(e) => { setTitle(e.target.value) }} value={title} className="form-control" id="title" name="title" />
                    </div>
                
                    <div className="mb-3">
                        <label className="form-label">Essay:</label>
                        <textarea onChange={(e) => { setEssay(e.target.value) }} value={essay} className="form-control" id="essay" name="essay" rows="5"></textarea>
                    </div>
                    <div className="d-grid gap-2">
                        <button onClick={fetchBarData} className="btn btn-warning btn-lg" type="submit">Submit</button>
                    </div>

                </form>

                <div className='barChart'>
                    {showBarChart ? <Bar data={data} options={options} /> : ""}
                </div>
            </div>

        </>
    )
}

