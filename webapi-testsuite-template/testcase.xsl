<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" version="1.0" encoding="UTF-8"
		indent="yes" />
	<xsl:template match="/">
		<html>
			<STYLE type="text/css">
				@import "result.css";
			</STYLE>

			<body>
				<div id="page">
					<div id="index_page">
						<div id="title">
							<table>
								<tr>
									<td class="title">
										<h1 align="center">Test Cases</h1>
									</td>
								</tr>
							</table>
						</div>
						<div id="suite">
							<xsl:for-each select="test_definition/suite">
								<xsl:sort select="@name" />
								<p>
									Test Suite:
									<xsl:value-of select="@name" />
								</p>
								<table>
									<tr>
										<th>Case_ID</th>
										<th>Purpose</th>
										<th>Type</th>
										<th>Component</th>
										<th>Execution Type</th>
										<th>Description</th>
										<th>Specification</th>
									</tr>
									<xsl:for-each select=".//set">
										<xsl:sort select="@name" />
										<tr>
											<td colspan="7">
												Test Set:
												<xsl:value-of select="@name" />
											</td>
										</tr>
										<xsl:for-each select=".//testcase">
											<xsl:sort select="@id" />
											<tr>
												<td>
													<xsl:value-of select="@id" />
												</td>
												<td>
													<xsl:value-of select="@purpose" />
												</td>
												<td>
													<xsl:value-of select="@type" />
												</td>
												<td>
													<xsl:value-of select="@component" />
												</td>
												<td>
													<xsl:value-of select="@execution_type" />
												</td>
												<td>
													<p>
														Pre_condition:
														<xsl:value-of select=".//description/pre_condition" />
													</p>
													<p>
														Post_condition:
														<xsl:value-of select=".//description/post_condition" />
													</p>
													<p>
														Test Script Entry:
														<xsl:value-of select=".//description/test_script_entry" />
													</p>
													<p>
														Steps:
														<p />
														<xsl:for-each select=".//description/steps/step">
															<xsl:sort select="@order" />
															Step<xsl:value-of select="@order" />:
															<xsl:value-of select="./step_desc" />;<p />
															Expected Result:
															<xsl:value-of select="./expected" />
															<p />
														</xsl:for-each>
													</p>
												</td>
												<td>
													<xsl:value-of select=".//spec" />
												</td>
											</tr>
										</xsl:for-each>
									</xsl:for-each>
								</table>
							</xsl:for-each>
						</div>
					</div>
				</div>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>