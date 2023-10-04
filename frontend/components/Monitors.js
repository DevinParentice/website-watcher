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

	const deleteElement = async (element) => {};
	const addElement = async (website) => {};

	return (
		<div className="max-w-screen-lg w-full">
			{data["monitors"]["websites"].map((website, i) => {
				return (
					<div key={i} className="p-4 bg-zinc-700 my-4">
						<div className="flex justify-between">
							<p>{website["name"]}</p>
							<div className="flex justify-around">
								<div className="flex gap-4 text-sm">
									<div className="bg-slate-500 rounded-md flex">
										<button
											onClick={() => addElement(website)}
											className=" bg-slate-600 h-full rounded-md px-2 text-xl"
										>
											&#43;
										</button>
									</div>
									{website["elements"].map((element, i) => {
										return (
											<div key={i} className="bg-slate-500 rounded-md flex">
												<div className="flex justify-center">
													<p className="py-1 px-3">{element["class"]}</p>
												</div>
												<button
													onClick={() => deleteElement(element)}
													className=" bg-slate-600 h-full rounded-r-md px-1"
												>
													&#10006;
												</button>
											</div>
										);
									})}
								</div>
								<button
									onClick={() => deleteMonitor(website)}
									className="ml-4 bg-red-400 px-2 rounded-md"
								>
									&#10006;
								</button>
							</div>
						</div>
					</div>
				);
			})}
		</div>
	);
}
