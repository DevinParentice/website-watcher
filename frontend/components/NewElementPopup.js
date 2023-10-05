"use client";

import { useState } from "react";

export default function NewElementPopup({
	siteName,
	setAddElementModalOpen,
	setMonitors,
}) {
	const [elementTag, setElementTag] = useState("");
	const [elementClass, setElementClass] = useState("");

	const createMonitor = async (e) => {
		e.preventDefault();

		const res = await fetch("http://127.0.0.1:5000/api/addElement", {
			method: "POST",
			mode: "cors",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				name: siteName,
				element: {
					tag: elementTag,
					class: elementClass,
				},
			}),
		});
		const body = await res.json();
		if (body.success) {
			setAddElementModalOpen(false);
			setMonitors(body.monitors);
		}
		return false;
	};

	return (
		<>
			<div
				className="fixed top-0 left-0 w-screen h-screen bg-black opacity-40 z-10"
				onClick={() => setAddElementModalOpen(false)}
			/>
			<div className="absolute top-0 left-0 flex w-screen h-screen justify-center items-center">
				<div className="relative max-w-6xl bg-zinc-700 z-10 px-8 py-4 rounded-lg">
					<div
						className="absolute right-2 top-2 cursor-pointer text-2xl px-4 font-semibold"
						onClick={() => setAddElementModalOpen(false)}
						tabIndex={0}
					>
						x
					</div>
					<h3 className="mb-4 text-xl">{"// Add an element to a Monitor"}</h3>
					<form className="flex flex-col w-96" onSubmit={createMonitor}>
						<label htmlFor="name" className="mb-1">
							Tag
						</label>
						<input
							type="text"
							name="name"
							id="name"
							value={elementTag}
							onChange={(e) => setElementTag(e.target.value)}
							placeholder="span"
							className="text-black p-1 rounded-sm mb-6"
						/>
						<label htmlFor="url" className="mb-1">
							Class
						</label>
						<input
							type="text"
							name="url"
							id="url"
							value={elementClass}
							onChange={(e) => setElementClass(e.target.value)}
							placeholder="product-price"
							className="text-black p-1 rounded-sm mb-6"
						/>
						<div className="flex justify-end">
							<button
								type="submit"
								className="bg-blue-500 py-1 px-4 rounded-md"
							>
								Submit
							</button>
						</div>
					</form>
				</div>
			</div>
		</>
	);
}
