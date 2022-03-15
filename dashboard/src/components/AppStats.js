import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://<host_name>/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Total of </th>
							<th>Stats</th>
						</tr>
						{/* <tr>
							<td># SNT: {stats['num_bp_readings']}</td>
							<td># MSK: {stats['num_hr_readings']}</td>
						</tr> */}
						<tr>
                            <th>sanitizer quantity:</th>
							<th>{stats['sanitizer_quantity']}</th>
							{/* <td colspan="2">sanitizer quantity: {stats['sanitizer_quantity']}</td> */}
						</tr>
						<tr>
                            <th>sanitizer price:</th>
							<th>{stats['sanitizer_price']}</th>
							{/* <td colspan="2">sanitizer price: {stats['sanitizer_price']}</td> */}
						</tr>
						<tr>
                            <th>mask quantity:</th>
							<th>{stats['mask_quantity']}</th>
							{/* <td colspan="2">mask quantity: {stats['mask_quantity']}</td> */}
						</tr>
                        <tr>
                            <th>mask price:</th>
							<th>{stats['mask_price']}</th>
							{/* <td colspan="2">mask price: {stats['mask_price']}</td> */}
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
