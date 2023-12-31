"use client";

import { useState } from "react";

export default function NewMonitorPopup({ setModalIsOpen, setMonitors }) {
	const [siteName, setSiteName] = useState("");
	const [siteUrl, setSiteUrl] = useState("");
	const [delay, setDelay] = useState("");
	const [newElements, setNewElements] = useState([{ tag: "", class: "" }]);

	const createMonitor = async (e) => {
		e.preventDefault();

		const res = await fetch("http://127.0.0.1:5000/api/addWebsite", {
			method: "POST",
			mode: "cors",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				name: siteName,
				url: siteUrl,
				delay: parseInt(delay),
				elements: newElements,
			}),
		});
		const body = await res.json();
		if (body.success) {
			setMonitors(body.monitors);
			setModalIsOpen(false);
			return true;
		}
		return false;
	};

	return (
		<>
			<div
				className="fixed top-0 left-0 w-screen h-screen bg-black opacity-40 z-10"
				onClick={() => setModalIsOpen(false)}
			/>
			<div className="absolute flex w-screen h-screen justify-center items-center">
				<div className="relative max-w-6xl bg-zinc-700 z-10 px-8 py-4 rounded-lg">
					<div
						className="absolute right-2 top-2 cursor-pointer text-2xl px-4 font-semibold"
						onClick={() => setModalIsOpen(false)}
						tabIndex={0}
					>
						x
					</div>
					<h3 className="mb-4 text-xl">{"// Create a new Monitor"}</h3>
					<form className="flex flex-col w-96" onSubmit={createMonitor}>
						<label htmlFor="name" className="mb-1">
							Name
						</label>
						<input
							type="text"
							name="name"
							id="name"
							value={siteName}
							onChange={(e) => setSiteName(e.target.value)}
							placeholder="My favorite site"
							className="text-black p-1 rounded-sm mb-6"
						/>
						<label htmlFor="url" className="mb-1">
							Website URL
						</label>
						<input
							type="text"
							name="url"
							id="url"
							value={siteUrl}
							onChange={(e) => setSiteUrl(e.target.value)}
							placeholder="https://www.example.com"
							className="text-black p-1 rounded-sm mb-6"
						/>
						<label htmlFor="delay" className="mb-1">
							Delay (in minutes)
						</label>
						<input
							type="tel"
							name="delay"
							id="delay"
							value={delay}
							onChange={(e) => setDelay(e.target.value)}
							placeholder="120"
							className="text-black p-1 rounded-sm mb-6"
						/>
						<div className="flex flex-col max-w-96">
							{newElements.map((element, i) => {
								return (
									<div key={i} className="flex">
										<div className="">
											<label htmlFor={`delay`} className="mb-1">
												Tag
											</label>
											<input
												type="tel"
												name={`tag-${i}`}
												id={`tag-${i}`}
												value={element.tag}
												onChange={(e) => {
													const updatedElements = newElements.map(
														(element, j) => {
															if (j === i) {
																return { ...element, tag: e.target.value };
															}
															return element;
														}
													);
													setNewElements(() => updatedElements);
												}}
												placeholder="span"
												className="text-black p-1 rounded-sm mr-4 w-full"
											/>
										</div>
										<div className="">
											<label htmlFor={`class-${i}`} className="mb-1 ml-6">
												Class
											</label>
											<input
												type="tel"
												name={`class-${i}`}
												id={`class-${i}`}
												value={element.class}
												onChange={(e) => {
													const updatedElements = newElements.map(
														(element, j) => {
															if (j === i) {
																return { ...element, class: e.target.value };
															}
															return element;
														}
													);
													setNewElements(() => updatedElements);
												}}
												placeholder="price-tag"
												className={`text-black p-1 rounded-sm ${
													i + 1 === newElements.length ? "mb-10" : "mb-2"
												} ml-6`}
											/>
										</div>
									</div>
								);
							})}
						</div>
						<div className="flex justify-between">
							<button
								type="button"
								className="bg-zinc-500 py-1 px-4 rounded-md"
								onClick={() =>
									setNewElements([...newElements, { tag: "", class: "" }])
								}
							>
								Add element
							</button>
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
