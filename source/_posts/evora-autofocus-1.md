---
title: 为36寸的大镜子写对焦程序
date: 2024-10-26 22:10:59
tags:
- 开发 
---

华盛顿大学 UW 有一台完全由本科学生维护的 36 英寸 RC 望远镜，我有幸混入了社团并且参与到软硬件的维护工作。

我上手的第一个大 feature 是为望远镜控制系统加入自动对焦，本文简述了这一目标的第一阶段 -- 基于数据的对焦辅助的开发过程和测试结果。

下面的内容摘自第一次实际测试后的小报告（并没人要求我写，只是觉得挺有意思的）

![（半）最终结果](cover.png)

<!-- more -->

{% raw %}
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><title>Evora Autofocus Phase I: Focus assist</title><style>
	/* cspell:disable-file */
	/* webkit printing magic: print all background colors */
	html {
		-webkit-print-color-adjust: exact;
	}
	* {
		box-sizing: border-box;
		-webkit-print-color-adjust: exact;
	}
	
	html,
	body {
		margin: 0;
		padding: 0;
	}
	
	body {
		line-height: 1.5;
		white-space: pre-wrap;
	}
	
	a,
	a.visited {
		color: inherit;
		text-decoration: underline;
	}
	
	.pdf-relative-link-path {
		font-size: 80%;
		color: #444;
	}
	
	h1,
	h2,
	h3 {
		letter-spacing: -0.01em;
		line-height: 1.2;
		font-weight: 600;
		margin-bottom: 0;
	}
	
	.page-title {
		font-size: 2.5rem;
		font-weight: 700;
		margin-top: 0;
		margin-bottom: 0.75em;
	}
	
	h1 {
		font-size: 1.875rem;
		margin-top: 1.875rem;
	}
	
	h2 {
		font-size: 1.5rem;
		margin-top: 1.5rem;
	}
	
	h3 {
		font-size: 1.25rem;
		margin-top: 1.25rem;
	}
	
	.source {
		border: 1px solid #ddd;
		border-radius: 3px;
		padding: 1.5em;
		word-break: break-all;
	}
	
	.callout {
		border-radius: 3px;
		padding: 1rem;
	}
	
	figure {
		margin: 1.25em 0;
		page-break-inside: avoid;
	}
	
	figcaption {
		opacity: 0.5;
		font-size: 85%;
		margin-top: 0.5em;
	}
	
	mark {
		background-color: transparent;
	}
	
	.indented {
		padding-left: 1.5em;
	}
	
	hr {
		background: transparent;
		display: block;
		width: 100%;
		height: 1px;
		visibility: visible;
		border: none;
		border-bottom: 1px solid rgba(55, 53, 47, 0.09);
	}
	
	img {
		max-width: 100%;
	}
	
	@media only print {
		img {
			max-height: 100vh;
			object-fit: contain;
		}
	}
	
	@page {
		margin: 1in;
	}
	
	.collection-content {
		font-size: 0.875rem;
	}
	
	.column-list {
		display: flex;
		justify-content: space-between;
	}
	
	.column {
		padding: 0 1em;
	}
	
	.column:first-child {
		padding-left: 0;
	}
	
	.column:last-child {
		padding-right: 0;
	}
	
	.table_of_contents-item {
		display: block;
		font-size: 0.875rem;
		line-height: 1.3;
		padding: 0.125rem;
	}
	
	.table_of_contents-indent-1 {
		margin-left: 1.5rem;
	}
	
	.table_of_contents-indent-2 {
		margin-left: 3rem;
	}
	
	.table_of_contents-indent-3 {
		margin-left: 4.5rem;
	}
	
	.table_of_contents-link {
		text-decoration: none;
		opacity: 0.7;
		border-bottom: 1px solid rgba(55, 53, 47, 0.18);
	}
	
	table,
	th,
	td {
		border: 1px solid rgba(55, 53, 47, 0.09);
		border-collapse: collapse;
	}
	
	table {
		border-left: none;
		border-right: none;
	}
	
	th,
	td {
		font-weight: normal;
		padding: 0.25em 0.5em;
		line-height: 1.5;
		min-height: 1.5em;
		text-align: left;
	}
	
	th {
		color: rgba(55, 53, 47, 0.6);
	}
	
	ol,
	ul {
		margin: 0;
		margin-block-start: 0.6em;
		margin-block-end: 0.6em;
	}
	
	li > ol:first-child,
	li > ul:first-child {
		margin-block-start: 0.6em;
	}
	
	ul > li {
		list-style: disc;
	}
	
	ul.to-do-list {
		padding-inline-start: 0;
	}
	
	ul.to-do-list > li {
		list-style: none;
	}
	
	.to-do-children-checked {
		text-decoration: line-through;
		opacity: 0.375;
	}
	
	ul.toggle > li {
		list-style: none;
	}
	
	ul {
		padding-inline-start: 1.7em;
	}
	
	ul > li {
		padding-left: 0.1em;
	}
	
	ol {
		padding-inline-start: 1.6em;
	}
	
	ol > li {
		padding-left: 0.2em;
	}
	
	.mono ol {
		padding-inline-start: 2em;
	}
	
	.mono ol > li {
		text-indent: -0.4em;
	}
	
	.toggle {
		padding-inline-start: 0em;
		list-style-type: none;
	}
	
	/* Indent toggle children */
	.toggle > li > details {
		padding-left: 1.7em;
	}
	
	.toggle > li > details > summary {
		margin-left: -1.1em;
	}
	
	.selected-value {
		display: inline-block;
		padding: 0 0.5em;
		background: rgba(206, 205, 202, 0.5);
		border-radius: 3px;
		margin-right: 0.5em;
		margin-top: 0.3em;
		margin-bottom: 0.3em;
		white-space: nowrap;
	}
	
	.collection-title {
		display: inline-block;
		margin-right: 1em;
	}
	
	.page-description {
		margin-bottom: 2em;
	}
	
	.simple-table {
		margin-top: 1em;
		font-size: 0.875rem;
		empty-cells: show;
	}
	.simple-table td {
		height: 29px;
		min-width: 120px;
	}
	
	.simple-table th {
		height: 29px;
		min-width: 120px;
	}
	
	.simple-table-header-color {
		background: rgb(247, 246, 243);
		color: black;
	}
	.simple-table-header {
		font-weight: 500;
	}
	
	time {
		opacity: 0.5;
	}
	
	.icon {
		display: inline-block;
		max-width: 1.2em;
		max-height: 1.2em;
		text-decoration: none;
		vertical-align: text-bottom;
		margin-right: 0.5em;
	}
	
	img.icon {
		border-radius: 3px;
	}
	
	.user-icon {
		width: 1.5em;
		height: 1.5em;
		border-radius: 100%;
		margin-right: 0.5rem;
	}
	
	.user-icon-inner {
		font-size: 0.8em;
	}
	
	.text-icon {
		border: 1px solid #000;
		text-align: center;
	}
	
	.page-cover-image {
		display: block;
		object-fit: cover;
		width: 100%;
		max-height: 30vh;
	}
	
	.page-header-icon {
		font-size: 3rem;
		margin-bottom: 1rem;
	}
	
	.page-header-icon-with-cover {
		margin-top: -0.72em;
		margin-left: 0.07em;
	}
	
	.page-header-icon img {
		border-radius: 3px;
	}
	
	.link-to-page {
		margin: 1em 0;
		padding: 0;
		border: none;
		font-weight: 500;
	}
	
	p > .user {
		opacity: 0.5;
	}
	
	td > .user,
	td > time {
		white-space: nowrap;
	}
	
	input[type="checkbox"] {
		transform: scale(1.5);
		margin-right: 0.6em;
		vertical-align: middle;
	}
	
	p {
		margin-top: 0.5em;
		margin-bottom: 0.5em;
	}
	
	.image {
		border: none;
		margin: 1.5em 0;
		padding: 0;
		border-radius: 0;
		text-align: center;
	}
	
	.code,
	code {
		background: rgba(135, 131, 120, 0.15);
		border-radius: 3px;
		padding: 0.2em 0.4em;
		border-radius: 3px;
		font-size: 85%;
		tab-size: 2;
	}
	
	code {
		color: #eb5757;
	}
	
	.code {
		padding: 1.5em 1em;
	}
	
	.code-wrap {
		white-space: pre-wrap;
		word-break: break-all;
	}
	
	.code > code {
		background: none;
		padding: 0;
		font-size: 100%;
		color: inherit;
	}
	
	blockquote {
		font-size: 1.25em;
		margin: 1em 0;
		padding-left: 1em;
		border-left: 3px solid rgb(55, 53, 47);
	}
	
	.bookmark {
		text-decoration: none;
		max-height: 8em;
		padding: 0;
		display: flex;
		width: 100%;
		align-items: stretch;
	}
	
	.bookmark-title {
		font-size: 0.85em;
		overflow: hidden;
		text-overflow: ellipsis;
		height: 1.75em;
		white-space: nowrap;
	}
	
	.bookmark-text {
		display: flex;
		flex-direction: column;
	}
	
	.bookmark-info {
		flex: 4 1 180px;
		padding: 12px 14px 14px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
	
	.bookmark-image {
		width: 33%;
		flex: 1 1 180px;
		display: block;
		position: relative;
		object-fit: cover;
		border-radius: 1px;
	}
	
	.bookmark-description {
		color: rgba(55, 53, 47, 0.6);
		font-size: 0.75em;
		overflow: hidden;
		max-height: 4.5em;
		word-break: break-word;
	}
	
	.bookmark-href {
		font-size: 0.75em;
		margin-top: 0.25em;
	}
	
	.sans { font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol"; }
	.code { font-family: "SFMono-Regular", Menlo, Consolas, "PT Mono", "Liberation Mono", Courier, monospace; }
	.serif { font-family: Lyon-Text, Georgia, ui-serif, serif; }
	.mono { font-family: iawriter-mono, Nitti, Menlo, Courier, monospace; }
	.pdf .sans { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol", 'Twemoji', 'Noto Color Emoji', 'Noto Sans CJK JP'; }
	.pdf:lang(zh-CN) .sans { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol", 'Twemoji', 'Noto Color Emoji', 'Noto Sans CJK SC'; }
	.pdf:lang(zh-TW) .sans { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol", 'Twemoji', 'Noto Color Emoji', 'Noto Sans CJK TC'; }
	.pdf:lang(ko-KR) .sans { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol", 'Twemoji', 'Noto Color Emoji', 'Noto Sans CJK KR'; }
	.pdf .code { font-family: Source Code Pro, "SFMono-Regular", Menlo, Consolas, "PT Mono", "Liberation Mono", Courier, monospace, 'Twemoji', 'Noto Color Emoji', 'Noto Sans Mono CJK JP'; }
	.pdf:lang(zh-CN) .code { font-family: Source Code Pro, "SFMono-Regular", Menlo, Consolas, "PT Mono", "Liberation Mono", Courier, monospace, 'Twemoji', 'Noto Color Emoji', 'Noto Sans Mono CJK SC'; }
	.pdf:lang(zh-TW) .code { font-family: Source Code Pro, "SFMono-Regular", Menlo, Consolas, "PT Mono", "Liberation Mono", Courier, monospace, 'Twemoji', 'Noto Color Emoji', 'Noto Sans Mono CJK TC'; }
	.pdf:lang(ko-KR) .code { font-family: Source Code Pro, "SFMono-Regular", Menlo, Consolas, "PT Mono", "Liberation Mono", Courier, monospace, 'Twemoji', 'Noto Color Emoji', 'Noto Sans Mono CJK KR'; }
	.pdf .serif { font-family: PT Serif, Lyon-Text, Georgia, ui-serif, serif, 'Twemoji', 'Noto Color Emoji', 'Noto Serif CJK JP'; }
	.pdf:lang(zh-CN) .serif { font-family: PT Serif, Lyon-Text, Georgia, ui-serif, serif, 'Twemoji', 'Noto Color Emoji', 'Noto Serif CJK SC'; }
	.pdf:lang(zh-TW) .serif { font-family: PT Serif, Lyon-Text, Georgia, ui-serif, serif, 'Twemoji', 'Noto Color Emoji', 'Noto Serif CJK TC'; }
	.pdf:lang(ko-KR) .serif { font-family: PT Serif, Lyon-Text, Georgia, ui-serif, serif, 'Twemoji', 'Noto Color Emoji', 'Noto Serif CJK KR'; }
	.pdf .mono { font-family: PT Mono, iawriter-mono, Nitti, Menlo, Courier, monospace, 'Twemoji', 'Noto Color Emoji', 'Noto Sans Mono CJK JP'; }
	.pdf:lang(zh-CN) .mono { font-family: PT Mono, iawriter-mono, Nitti, Menlo, Courier, monospace, 'Twemoji', 'Noto Color Emoji', 'Noto Sans Mono CJK SC'; }
	.pdf:lang(zh-TW) .mono { font-family: PT Mono, iawriter-mono, Nitti, Menlo, Courier, monospace, 'Twemoji', 'Noto Color Emoji', 'Noto Sans Mono CJK TC'; }
	.pdf:lang(ko-KR) .mono { font-family: PT Mono, iawriter-mono, Nitti, Menlo, Courier, monospace, 'Twemoji', 'Noto Color Emoji', 'Noto Sans Mono CJK KR'; }
	.highlight-default {
		color: rgba(55, 53, 47, 1);
	}
	.highlight-gray {
		color: rgba(120, 119, 116, 1);
		fill: rgba(120, 119, 116, 1);
	}
	.highlight-brown {
		color: rgba(159, 107, 83, 1);
		fill: rgba(159, 107, 83, 1);
	}
	.highlight-orange {
		color: rgba(217, 115, 13, 1);
		fill: rgba(217, 115, 13, 1);
	}
	.highlight-yellow {
		color: rgba(203, 145, 47, 1);
		fill: rgba(203, 145, 47, 1);
	}
	.highlight-teal {
		color: rgba(68, 131, 97, 1);
		fill: rgba(68, 131, 97, 1);
	}
	.highlight-blue {
		color: rgba(51, 126, 169, 1);
		fill: rgba(51, 126, 169, 1);
	}
	.highlight-purple {
		color: rgba(144, 101, 176, 1);
		fill: rgba(144, 101, 176, 1);
	}
	.highlight-pink {
		color: rgba(193, 76, 138, 1);
		fill: rgba(193, 76, 138, 1);
	}
	.highlight-red {
		color: rgba(212, 76, 71, 1);
		fill: rgba(212, 76, 71, 1);
	}
	.highlight-gray_background {
		background: rgba(241, 241, 239, 1);
	}
	.highlight-brown_background {
		background: rgba(244, 238, 238, 1);
	}
	.highlight-orange_background {
		background: rgba(251, 236, 221, 1);
	}
	.highlight-yellow_background {
		background: rgba(251, 243, 219, 1);
	}
	.highlight-teal_background {
		background: rgba(237, 243, 236, 1);
	}
	.highlight-blue_background {
		background: rgba(231, 243, 248, 1);
	}
	.highlight-purple_background {
		background: rgba(244, 240, 247, 0.8);
	}
	.highlight-pink_background {
		background: rgba(249, 238, 243, 0.8);
	}
	.highlight-red_background {
		background: rgba(253, 235, 236, 1);
	}
	.block-color-default {
		color: inherit;
		fill: inherit;
	}
	.block-color-gray {
		color: rgba(120, 119, 116, 1);
		fill: rgba(120, 119, 116, 1);
	}
	.block-color-brown {
		color: rgba(159, 107, 83, 1);
		fill: rgba(159, 107, 83, 1);
	}
	.block-color-orange {
		color: rgba(217, 115, 13, 1);
		fill: rgba(217, 115, 13, 1);
	}
	.block-color-yellow {
		color: rgba(203, 145, 47, 1);
		fill: rgba(203, 145, 47, 1);
	}
	.block-color-teal {
		color: rgba(68, 131, 97, 1);
		fill: rgba(68, 131, 97, 1);
	}
	.block-color-blue {
		color: rgba(51, 126, 169, 1);
		fill: rgba(51, 126, 169, 1);
	}
	.block-color-purple {
		color: rgba(144, 101, 176, 1);
		fill: rgba(144, 101, 176, 1);
	}
	.block-color-pink {
		color: rgba(193, 76, 138, 1);
		fill: rgba(193, 76, 138, 1);
	}
	.block-color-red {
		color: rgba(212, 76, 71, 1);
		fill: rgba(212, 76, 71, 1);
	}
	.block-color-gray_background {
		background: rgba(241, 241, 239, 1);
	}
	.block-color-brown_background {
		background: rgba(244, 238, 238, 1);
	}
	.block-color-orange_background {
		background: rgba(251, 236, 221, 1);
	}
	.block-color-yellow_background {
		background: rgba(251, 243, 219, 1);
	}
	.block-color-teal_background {
		background: rgba(237, 243, 236, 1);
	}
	.block-color-blue_background {
		background: rgba(231, 243, 248, 1);
	}
	.block-color-purple_background {
		background: rgba(244, 240, 247, 0.8);
	}
	.block-color-pink_background {
		background: rgba(249, 238, 243, 0.8);
	}
	.block-color-red_background {
		background: rgba(253, 235, 236, 1);
	}
	.select-value-color-uiBlue { background-color: rgba(35, 131, 226, .07); }
	.select-value-color-pink { background-color: rgba(245, 224, 233, 1); }
	.select-value-color-purple { background-color: rgba(232, 222, 238, 1); }
	.select-value-color-green { background-color: rgba(219, 237, 219, 1); }
	.select-value-color-gray { background-color: rgba(227, 226, 224, 1); }
	.select-value-color-translucentGray { background-color: rgba(255, 255, 255, 0.0375); }
	.select-value-color-orange { background-color: rgba(250, 222, 201, 1); }
	.select-value-color-brown { background-color: rgba(238, 224, 218, 1); }
	.select-value-color-red { background-color: rgba(255, 226, 221, 1); }
	.select-value-color-yellow { background-color: rgba(253, 236, 200, 1); }
	.select-value-color-blue { background-color: rgba(211, 229, 239, 1); }
	.select-value-color-pageGlass { background-color: undefined; }
	.select-value-color-washGlass { background-color: undefined; }
	
	.checkbox {
		display: inline-flex;
		vertical-align: text-bottom;
		width: 16;
		height: 16;
		background-size: 16px;
		margin-left: 2px;
		margin-right: 5px;
	}
	
	.checkbox-on {
		background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%0A%3Crect%20width%3D%2216%22%20height%3D%2216%22%20fill%3D%22%2358A9D7%22%2F%3E%0A%3Cpath%20d%3D%22M6.71429%2012.2852L14%204.9995L12.7143%203.71436L6.71429%209.71378L3.28571%206.2831L2%207.57092L6.71429%2012.2852Z%22%20fill%3D%22white%22%2F%3E%0A%3C%2Fsvg%3E");
	}
	
	.checkbox-off {
		background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%0A%3Crect%20x%3D%220.75%22%20y%3D%220.75%22%20width%3D%2214.5%22%20height%3D%2214.5%22%20fill%3D%22white%22%20stroke%3D%22%2336352F%22%20stroke-width%3D%221.5%22%2F%3E%0A%3C%2Fsvg%3E");
	}
		
	</style></head><body><article id="047602db-5bed-4461-abdd-153247c1272a" class="page sans"><header><h1 class="page-title">Evora Autofocus Phase I: Focus assist</h1><p class="page-description"></p></header><div class="page-body"><figure id="e3d343e0-9ffc-4c3a-ab05-5eb00e4623bd"><a href="https://github.com/siyu6974/evora_autofocus#usage-version-01-awful-architecture-i-know-d" class="bookmark source"><div class="bookmark-info"><div class="bookmark-text"><div class="bookmark-title">GitHub - siyu6974/evora_autofocus</div><div class="bookmark-description">Contribute to siyu6974/evora_autofocus development by creating an account on GitHub.</div></div><div class="bookmark-href"><img src="https://github.com/fluidicon.png" class="icon bookmark-icon"/>https://github.com/siyu6974/evora_autofocus#usage-version-01-awful-architecture-i-know-d</div></div><img src="https://opengraph.githubassets.com/cf69b604b32e01e351e6caab318ee4639ad5b93ab31a6d6df1620b0ce8390fd6/siyu6974/evora_autofocus" class="bookmark-image"/></a></figure><h1 id="967268d3-0288-4c09-a3db-4efec7f93bdf" class="">Method</h1><ul id="628359cf-e6a7-449f-bac8-d41f5fddd1dc" class="bulleted-list"><li style="list-style-type:disc">FWHM<ul id="fb0b6899-b792-4ed0-943c-39267eef5a95" class="bulleted-list"><li style="list-style-type:circle">Full width half maximum</li></ul><ul id="482e5d50-3b23-447e-97b1-cfad98428878" class="bulleted-list"><li style="list-style-type:circle">Astropy has it </li></ul><div id="1846dec7-e565-4286-b274-6389f8e8da9c" class="column-list"><div id="ac614982-5aa8-4556-833a-26ac88295c8d" style="width:100%" class="column"><figure id="cbd3ca73-89ff-4c02-8c12-4dd6e58b4650" class="image"><a href="Untitled1.png"><img style="width:309px" src="Untitled1.png"/></a></figure></div><div id="50dce058-a418-4a07-b640-4754d383ac48" style="width:100%" class="column"><p id="e66a4577-7ca7-4200-b065-a43a7dbeed80" class="">
	</p><figure id="2343f10a-5782-4fba-a803-e43e4a6a6516" class="image"><a href="Untitled2.png"><img style="width:640px" src="Untitled2.png"/></a><figcaption><a href="https://www.lost-infinity.com/night-sky-image-processing-part-5-measuring-fwhm-of-a-star-using-curve-fitting-a-simple-c-implementation/">https://www.lost-infinity.com/night-sky-image-processing-part-5-measuring-fwhm-of-a-star-using-curve-fitting-a-simple-c-implementation/</a></figcaption></figure></div></div></li></ul><ul id="e22cf35c-c3ba-4420-8869-a5d726ecb5b6" class="bulleted-list"><li style="list-style-type:disc">HFD / HFR<ul id="00b73147-0eb5-4ae5-951a-7e48434fb9ba" class="bulleted-list"><li style="list-style-type:circle">Half flux diameter or radius </li></ul><ul id="af9792f1-d77a-4127-93b1-96e4557a71da" class="bulleted-list"><li style="list-style-type:circle">general concept<ul id="54bba351-8086-468f-a025-82f5fecdd66d" class="bulleted-list"><li style="list-style-type:square"><a href="https://www.lost-infinity.com/night-sky-image-processing-part-6-measuring-the-half-flux-diameter-hfd-of-a-star-a-simple-c-implementation/">https://www.lost-infinity.com/night-sky-image-processing-part-6-measuring-the-half-flux-diameter-hfd-of-a-star-a-simple-c-implementation/</a></li></ul><ul id="229ede28-0961-4dc7-8f95-990bd52f13bb" class="bulleted-list"><li style="list-style-type:square"><a href="http://www.ccdware.com/Files/ITS%20Paper.pdf">http://www.ccdware.com/Files/ITS Paper.pdf</a></li></ul><ul id="280c7c0c-eab1-49e3-8abe-f598a204ae47" class="bulleted-list"><li style="list-style-type:square">more tolerant to out of focus star, especially for cassegrain </li></ul></li></ul><ul id="f1f01e75-6dd7-4edb-ae60-355204da9a88" class="bulleted-list"><li style="list-style-type:circle">Implementation to achieve better sub pixel accuracy, not yet implemented<ul id="7fc5b7c7-5874-4f17-905b-9cd738a57882" class="bulleted-list"><li style="list-style-type:square">sorting based <a href="https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L83">https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L83</a></li></ul><ul id="c6f7f8fc-1bfa-4d73-ac86-eeadcbea10f4" class="bulleted-list"><li style="list-style-type:square">interpolation based: NINA <a href="https://bitbucket.org/Isbeorn/nina/src/master/NINA.Core.WPF/ViewModel/AutoFocus/">https://bitbucket.org/Isbeorn/nina/src/master/NINA.Core.WPF/ViewModel/AutoFocus/</a></li></ul></li></ul></li></ul><h1 id="6ee5ee24-cea5-4662-a8c8-381e9883dc2e" class="">Evora image test</h1><p id="943714ae-263c-4f76-acb4-5f55107e2baa" class="">This was to test star detection and the correlation between FWHM and HFD on evora images. Test image <code>2023-05-20T09-32-28_r_-81.19_250.0s_r.fits</code></p><figure id="7fe6e936-9760-41ee-a8dd-9c27ce244373"><div class="source"><a href="single_image_test.ipynb">single_image_test.ipynb</a></div></figure><div id="9ce66ca7-145b-4bdb-b789-170a78da14e1" class="column-list"><div id="4b76b1b9-3e0e-4932-ac5f-a22b0b10b6a1" style="width:50%" class="column"><figure id="04378f4c-fb98-4345-bdbc-0174ea58fcb8" class="image"><a href="Untitled3.png"><img style="width:843px" src="Untitled3.png"/></a></figure></div><div id="818fcbdb-d6b9-427e-94a8-7d33799f32c1" style="width:50%" class="column"><figure id="ceb33dff-d4c1-40ea-8e0a-c8460f54766f" class="image"><a href="Untitled4.png"><img style="width:565px" src="Untitled4.png"/></a></figure></div></div><p id="cf2a00f5-3658-49a1-945f-271476ec7549" class="">The DAOStarFinder seems fine. FWHM is fairly consistent across the image. HFD has some weird negative values but the overall trend correlates with FWHM so it’s good. </p><h1 id="988f6e88-4581-458b-98f0-3de44cfe2f7f" class="">Home test</h1><p id="25143d4c-d9a2-4545-962a-6a1bbecfcaae" class="">Prior to the field test, a test was conducted at home to validate the method and general implementation of the algorithm.  </p><p id="f7c02e9c-35cb-4e9b-9890-cf90dffd2bd0" class="">The optic train consists of a Askar 65phq telescope (D=65mm, F/6.4) and a Qhy533M cooled CMOS camera. <del>Data was collected while performing auto focus routine in NINA with hocus focus plugin. </del> Focus was adjusted manually by commanding the ZWO EAF to advance inward and outward. The sweep was not mono-directional but backlash should be compensated automatically by NINA. After each movement, a 2 second exposure was taken with L filter. </p><figure id="6836dcc4-7f2c-4348-ade1-04396206ad90"><div class="source"><a href="focus_test.ipynb">focus_test.ipynb</a></div></figure><div id="bbdd5eb8-3a94-4344-9b3c-118230f2b6a9" class="column-list"><div id="402ded95-c818-4158-98b3-31ceed236e56" style="width:33.333333333333336%" class="column"><figure id="e28fc300-81af-4dff-af9a-7fe6fd61152a" class="image"><a href="Untitled5.png"><img style="width:546px" src="Untitled5.png"/></a><figcaption>nice round tight stars</figcaption></figure></div><div id="a694cad7-22c1-4b40-8d13-e9b3d4b1606d" style="width:33.33333333333333%" class="column"><figure id="d8b2b1df-9d76-431c-b42e-1eb113f1a9ad" class="image"><a href="Untitled6.png"><img style="width:537px" src="Untitled6.png"/></a><figcaption>out of focus example</figcaption></figure></div><div id="1fdd3ee9-42f5-4211-9dcc-d034501f8872" style="width:33.333333333333336%" class="column"><figure id="613be112-792f-454f-a8d8-8a5cec1516b3" class="image"><a href="Untitled7.png"><img style="width:954px" src="Untitled7.png"/></a><figcaption>FWHM predicted 13678.46<br/>HFD predicted 13670.96<br/></figcaption></figure></div></div><p id="f818a335-e0bc-40a9-8565-9f0747053298" class="">Results given by hocus focus on 2 others runs 2 hours later: 13636 for R, 13701 for L. </p><p id="129eec37-7ff5-4504-8217-0834009789ef" class="">Without any modification to HFD calculation, the negative numbers disappeared. Great?</p><p id="6010e5cc-daae-49fb-849f-cc812a658364" class="">Near the focus point, HFDs were almost flat, which is probably caused by the lack of precision of the current implementation. Need to go sub pixel.  </p><h1 id="345043c2-d551-453a-92e4-62709f30688f" class="">MRO field test</h1><h2 id="0ad58f55-b876-4d31-b5be-9a2d5b4ec0ed" class="">Initial test on 5s V-band exposures</h2><figure id="6be42b98-6177-416e-abfd-1439be39659d" class="image"><a href="Screenshot_2023-10-25_at_16.54.38.png"><img style="width:1442px" src="Screenshot_2023-10-25_at_16.54.38.png"/></a></figure><p id="88873eb8-1508-4333-8f6b-d958211daa8e" class="">Initial result was awful. 2 fits didn’t agree with each other, HFD values were nonsense. FWHM were also off, even if we excluded the outliner. </p><p id="ef6dc5ef-cb26-4189-becf-76ed0232343e" class="">Checking the intermediate steps, the DAOStarFinder was picking noise as stars. Tuning the parameters (#brightest, fwhm, std) didn’t help at all, and the selection was not consistent across the sweep. </p><h2 id="a7172152-3aa0-44ae-8553-6e765f4bfee0" class="">Hot fix with sep - thanks José!</h2><figure id="55c9317d-33b5-4521-80f9-5b2dd711fafd"><div class="source"><a href="mro_single_image_test.ipynb">mro_single_image_test.ipynb</a></div></figure><figure id="d8fd6414-57d9-4e4b-8d73-d17a83180b32"><div class="source"><a href="mro_first_field_test.ipynb">mro_first_field_test.ipynb</a></div></figure><div id="8c847eaf-7d80-4b5d-8431-72f070dccace" class="column-list"><div id="88fd19a1-455e-4b93-a96c-1e28aa095c84" style="width:33.33333333333333%" class="column"><figure id="e54f6cd9-17ae-4db4-aee2-cdff1546e39b" class="image"><a href="Untitled8.png"><img style="width:515px" src="Untitled8.png"/></a><figcaption>comma or seeing?</figcaption></figure></div><div id="ef516c72-8978-4720-81e3-81e60c5ffabd" style="width:33.333333333333336%" class="column"><figure id="a1cf0d4c-11d5-442c-84e9-1e8adb06acec" class="image"><a href="Untitled9.png"><img style="width:518px" src="Untitled9.png"/></a></figure></div><div id="cedfb211-8b39-4274-bc8f-5c237ecc068e" style="width:33.333333333333336%" class="column"><figure id="e0a5a14f-8ba3-4912-84e9-c9eb00f6f14e" class="image"><a href="Untitled10.png"><img style="width:524px" src="Untitled10.png"/></a><figcaption>sep thinks this is 40pix big</figcaption></figure></div></div><p id="fa215072-08a9-487e-8990-40a7f02b0a7c" class="">Sep worked wonder, with min-pix it’s even like black magic. This finally allowed the following calculation to work.</p><p id="69ab8d11-ff66-4ab6-8bd0-0f5a0210f003" class="">Stars are in bad shape, not sure if it’s seeing that’s tearing them apart. Longer exposure should help but takes more patience…</p><figure id="c45c6ff4-40c3-4ac8-8874-add85acca24b" class="image"><a href="Untitled11.png"><img style="width:989px" src="Untitled11.png"/></a></figure><p id="79111868-2151-4834-8dcd-18e725f2898b" class="">HFD values are completely unusable, guess the noise was fooling my naive implementation. But FWHM seems like an OK fit.</p><h2 id="75319872-ee1f-4b86-9fa8-40e0649db4dd" class="">Real exposure</h2><div id="8d4cd1f9-57f6-41e5-8c62-821f7c583f2a" class="column-list"><div id="c06623b3-6952-4d7d-b671-ac40727b353f" style="width:50%" class="column"><figure id="feba9b1a-f8b2-4388-b5bd-b2259c1f2f3d" class="image"><a href="Untitled12.png"><img style="width:989px" src="Untitled12.png"/></a><figcaption>Eyeballed. 2023-10-21T08-57-43_B_-79.25_60.0s_0071.fits. FWHM: 4.2</figcaption></figure></div><div id="c1f69966-2bd8-4d34-b2dd-9ffa78208e56" style="width:50%" class="column"><figure id="73acdfa3-3e2d-4614-aea5-cee11c781064" class="image"><a href="cover.png"><img style="width:989px" src="cover.png"/></a><figcaption>Calculated. 2023-10-21T09-00-13_B_-79.25_60.0s_0072.fits. FWHM: 3.0</figcaption></figure></div></div><p id="8e0369c6-db2a-4a5d-8e55-5e2a649295c8" class="">Much better!</p><p id="0bd5132c-52a3-4273-8f3c-d525b760fc0e" class="">Note: the focuser position was calculated on V band, the above exposure was on B so the final image could be even better.</p><p id="dfb1153a-e7a1-4905-a28a-b6d241209c34" class="">
	</p><h1 id="24d7df61-4256-4a4c-8951-66d5c2a2ccc4" class="">TODO</h1><ul id="8c59721f-de5c-4927-a538-adc6b184d7f1" class="to-do-list"><li><div class="checkbox checkbox-off"></div> <span class="to-do-children-unchecked">sweep all filters, make an offset table</span><div class="indented"></div></li></ul><ul id="b1beee06-9db4-4467-83c3-c5b4895d3f4c" class="to-do-list"><li><div class="checkbox checkbox-off"></div> <span class="to-do-children-unchecked">make better UI &amp; integrate into evora</span><div class="indented"></div></li></ul><ul id="74d2c332-dd58-433e-864c-1db3d3763d64" class="to-do-list"><li><div class="checkbox checkbox-off"></div> <span class="to-do-children-unchecked">sub pixel HFD</span><div class="indented"></div></li></ul><h1 id="4c5063fc-1447-4296-a9d4-52c0e6049854" class="">After first field test</h1><p id="ef330ef0-e250-4aca-85e8-bb6c468b2db4" class=""><time>@October 31, 2023</time> </p><p id="b54881ae-9740-4e13-80d1-4247310ec3e6" class="">The hot fix using SEP and parameters that worked at MRO doesn’t work for my setup</p><ul id="74c3dfd2-fadb-46a6-8f87-a486da0970a5" class="bulleted-list"><li style="list-style-type:disc">Too many stars</li></ul><ul id="079ce5a8-34c9-4b0a-9124-8f32b085e4d3" class="bulleted-list"><li style="list-style-type:disc">FWHM fit can produce extreme outliers</li></ul><p id="4421c9ef-24f2-4ded-b05d-121c39e4c4ef" class="">Solutions</p><ul id="a7bbbe25-7ad7-40a7-88aa-d30bc3ce5e91" class="bulleted-list"><li style="list-style-type:disc">limit source extraction output</li></ul><ul id="86bef35b-f722-4d10-84bf-8a64723bee22" class="bulleted-list"><li style="list-style-type:disc">use median FWHM </li></ul><p id="c6fbb239-0eb9-4e18-a494-18aee7668213" class="">HFD</p><ul id="75b703db-52cb-4b36-983a-3ff4fa167044" class="bulleted-list"><li style="list-style-type:disc">Issue with previous HFD calculation: pixel distance set to the top left corner of the aperture, should be the center</li></ul><ul id="a7ac7ac0-5ece-426a-ad85-343a91ffd30b" class="bulleted-list"><li style="list-style-type:disc">Phd2 implementation: <a href="https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L113">https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L11</a><a href="https://github.com/OpenPHDGuiding/phd2/blob/5576bc0832c78b009e30687ac6b30404cb9e8fcd/star.cpp#L83">3</a></li></ul><ul id="4f2cbcae-af1e-4f8b-a0e4-9678ecc4ad5e" class="bulleted-list"><li style="list-style-type:disc"><code><strong>sep.flux_radius</strong></code><strong> is fast </strong></li></ul><div id="c73b9e0b-447f-48cb-8601-9f5b49a57646" class="column-list"><div id="e2ae957a-2e34-4c2e-9905-f96f2deca854" style="width:50.000000000000014%" class="column"><figure id="fae3db8f-5c27-408d-8680-de9e3c0f869c" class="image"><a href="Untitled13.png"><img style="width:989px" src="Untitled13.png"/></a><figcaption>previous</figcaption></figure></div><div id="4cae7bbb-fc56-4021-b319-3fc9bd5aa7a4" style="width:50%" class="column"><figure id="17ffca7c-6459-47b7-9a7d-f982c086cb3b" class="image"><a href="Untitled14.png"><img style="width:989px" src="Untitled14.png"/></a><figcaption>sep extraction, median</figcaption></figure><p id="92a454ec-fa78-4361-b790-020281add3ee" class="">
	</p></div></div></article><span class="sans" style="font-size:14px;padding-top:2em"></span></body>
</html>
{% endraw %}
