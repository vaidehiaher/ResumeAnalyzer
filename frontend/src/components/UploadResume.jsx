import { useState } from "react";
import API from "../api/api";

function UploadResume({ setAnalysis }) {

    const [resume, setResume] = useState(null);

    const [jobDescription, setJobDescription] = useState("");

    const [uploading, setUploading] = useState(false);

    const [analyzing, setAnalyzing] = useState(false);


    // -----------------------------------------
    // Upload Resume
    // -----------------------------------------

    const uploadResume = async () => {

        if (!resume) {
            alert("Please select a resume");
            return;
        }

        const formData = new FormData();

        formData.append(
            "resume",
            resume
        );

        try {

            setUploading(true);

            await API.post(
                "/upload-resume",
                formData,
                {
                    headers: {
                        Authorization:
                            "Bearer " +
                            localStorage.getItem("token"),

                        "Content-Type":
                            "multipart/form-data"
                    }
                }
            );

            alert(
                "Resume uploaded successfully"
            );

        }

        catch (err) {

            console.log(err);

            alert(
                err.response?.data?.message ||
                "Upload Failed"
            );

        }

        finally {

            setUploading(false);

        }
    };


    // -----------------------------------------
    // Analyze Resume
    // -----------------------------------------

    const analyzeResume = async () => {

        if (!resume) {

            alert(
                "Please upload a resume first"
            );

            return;
        }

        if (jobDescription.trim() === "") {

            alert(
                "Enter Job Description"
            );

            return;
        }

        try {

            setAnalyzing(true);

            const res = await API.post(

                "/analyze",

                {
                    job_description:
                        jobDescription
                },

                {
                    headers: {
                        Authorization:
                            "Bearer " +
                            localStorage.getItem("token")
                    }
                }

            );

            console.log(
                "Analysis Response"
            );

            console.log(
                res.data
            );

            setAnalysis(
                res.data
            );

        }

        catch (err) {

            console.log(err);

            console.log(
                err.response
            );

            console.log(
                err.response?.data
            );

            alert(
                err.response?.data?.message ||
                JSON.stringify(
                    err.response?.data
                ) ||
                "Analysis Failed"
            );

        }

        finally {

            setAnalyzing(false);

        }
    };


    // -----------------------------------------
    // UI
    // -----------------------------------------

    return (

        <div className="card shadow p-4">

            <h3>
                Resume Analyzer
            </h3>


            {/* Resume Upload */}

            <input

                type="file"

                className="form-control mt-3"

                accept=".pdf"

                onChange={(e) =>
                    setResume(
                        e.target.files[0]
                    )
                }

                disabled={
                    uploading ||
                    analyzing
                }

            />


            {/* Upload Button */}

            <button

                className="btn btn-primary mt-3"

                onClick={uploadResume}

                disabled={
                    uploading ||
                    analyzing
                }

            >

                {uploading
                    ? "Uploading..."
                    : "Upload Resume"
                }

            </button>


            {/* Job Description */}

            <textarea

                className="form-control mt-4"

                rows="8"

                placeholder="Paste Job Description"

                value={jobDescription}

                onChange={(e) =>
                    setJobDescription(
                        e.target.value
                    )
                }

                disabled={
                    uploading ||
                    analyzing
                }

            />


            {/* Analyze Button */}

            <button

                className="btn btn-success mt-3"

                onClick={analyzeResume}

                disabled={
                    uploading ||
                    analyzing
                }

            >

                {analyzing
                    ? "🤖 Analyzing with AI..."
                    : "Analyze Resume"
                }

            </button>


            {/* Loading Message */}

            {analyzing && (

                <div className="text-center mt-3">

                    <div
                        className="spinner-border text-success"
                        role="status"
                    >
                    </div>

                    <p className="mt-2">

                        Analyzing your resume
                        against the job description...

                        <br />

                        This may take a few seconds.

                    </p>

                </div>

            )}

        </div>

    );
}

export default UploadResume;