import { useState } from "react";

import Navbar from "../components/Navbar";
import UploadResume from "../components/UploadResume";
import ATSCard from "../components/ATSCard";
import SkillsCard from "../components/SkillsCard";
import Suggestions from "../components/Suggestions";


function Dashboard() {

    const [analysis, setAnalysis] = useState(null);

    return (

        <>

            <Navbar />

            <div className="container mt-4">

                {/* Resume Upload */}
                <UploadResume
                    analysis={analysis}
                    setAnalysis={setAnalysis}
                />

                <br />

                {analysis && (
                    <>

                        {/* ATS Score */}
                        <ATSCard analysis={analysis} />

                        <br />

                        {/* Skills */}
                        <SkillsCard analysis={analysis} />

                        <br />

                        {/* AI Summary */}
                        <div className="card shadow-sm mb-4">

                            <div className="card-body">

                                <h4 className="card-title">
                                    🤖 AI Resume Summary
                                </h4>

                                <hr />

                                <p className="card-text">
                                    {analysis.summary ||
                                        "No AI summary available."}
                                </p>

                            </div>

                        </div>

                        {/* AI Suggestions */}
                        <Suggestions analysis={analysis} />

                    </>
                )}

            </div>

        </>

    );
}


export default Dashboard;