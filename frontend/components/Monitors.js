"use client";

export default function Monitors(data) {
	const deleteMonitor = async (website) => {
		const res = await fetch("http://127.0.0.1:5000/api/deleteWebsite", {
			method: "DELETE",
			mode: "cors",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				name: website["name"],
			}),
		});
		const body = await res.json();
		console.log(body);
		if (body.success) {
			return true;
		}
		return false;
	};

	return (
		<div className="max-w-screen-lg w-full">
			{data["monitors"]["websites"].map((website, i) => {
				return (
					<div key={i} className="p-4 bg-zinc-700 my-4">
						<div className="flex justify-between">
							<p>{website["name"]}</p>
							<button onClick={() => deleteMonitor(website)}>x</button>
						</div>
					</div>
				);
			})}
		</div>
	);
}
