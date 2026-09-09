function SkillsCard({ analysis }) {

    return (

        <div className="card shadow mt-4">

            <div className="card-body">

                <div className="row">

                    <div className="col-md-6">

                        <h4>

                            ✅ Matched Skills

                        </h4>

                        {

                            analysis.matched_skills.map(

                                (skill, index) => (

                                    <span

                                        key={index}

                                        className="badge bg-success me-2 mb-2"

                                    >

                                        {skill}

                                    </span>

                                )

                            )

                        }

                    </div>

                    <div className="col-md-6">

                        <h4>

                            ❌ Missing Skills

                        </h4>

                        {

                            analysis.missing_skills.map(

                                (skill, index) => (

                                    <span

                                        key={index}

                                        className="badge bg-danger me-2 mb-2"

                                    >

                                        {skill}

                                    </span>

                                )

                            )

                        }

                    </div>

                </div>

            </div>

        </div>

    );

}

export default SkillsCard;