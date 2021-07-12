using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http.Headers;
using System.Threading;
using System.Threading.Tasks;
using Application.Data.Repositories;
using Application.Mapping.Model;
using Contracts;
using Contracts.Request;
using Contracts.Response;
using Domain.DataTransfer;
using Domain.Entities;
using Domain.ValueObjects;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace ModelAPI.Controllers
{
    [ApiController]
    public class TFLiteRecordController : ControllerBase
    {
        private readonly ITFLiteRecordRepository _tFLiteRecordRepository;
        private readonly ITFLiteRecordRequestMapper _requestMapper;
        private readonly ITFLiteRecordResponseMapper _responseMapper;
        private readonly ILogger _logger;

        public TFLiteRecordController(ITFLiteRecordRepository tFLiteRecordRepository,
            ITFLiteRecordRequestMapper requestMapper,
            ITFLiteRecordResponseMapper responseMapper)
        {
            _tFLiteRecordRepository = tFLiteRecordRepository;
            _requestMapper = requestMapper;
            _responseMapper = responseMapper;
        }

        [HttpGet(ApiRoutes.Model.GetAll)]
        [ProducesResponseType(typeof(EnumerableEnvelope<TFLiteRecordGetAllDto>), StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll([FromQuery] PaginationRequestDto paginationRequestDto)
        {
            var pagination = _requestMapper.MapPaginationRequest(paginationRequestDto);

            var envelope = await _tFLiteRecordRepository.GetAllAsync(pagination);

            var responseEnvelope = _responseMapper.MapGetAllResponse(envelope);

            return Ok(responseEnvelope);
        }

        [HttpGet(ApiRoutes.Model.GetById)]
        public async Task<IActionResult> GetById(int id)
        {
            byte[] zipContent = await _tFLiteRecordRepository.GetByIdAsync(id);

            if (zipContent == null)
            {
                return NotFound();
            }

            return File(zipContent, "application/zip", "record.zip");
        }

        [HttpPost(ApiRoutes.Model.Create)]
        [ProducesResponseType(StatusCodes.Status201Created)]
        public async Task<IActionResult> UploadModel(IFormFile model, IFormFile label)
        {
            string modelName = Path.GetFileName(model.FileName);
            FormFileZipper zipper = _requestMapper.MapCreateRequest(model, label);
            
            int id = await _tFLiteRecordRepository.CreateAsync(modelName, zipper);


            return CreatedAtAction(nameof(GetById), new { id }, null);
        }

        [HttpDelete(ApiRoutes.Model.Delete)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        public async Task<IActionResult> Delete(int id)
        {
            await _tFLiteRecordRepository.DeleteAsync(id);

            return NoContent();
        }
    }
}
